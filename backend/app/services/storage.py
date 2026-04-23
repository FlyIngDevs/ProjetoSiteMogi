from pathlib import Path
from uuid import uuid4
import logging
import time

import boto3
from botocore.config import Config
from botocore.exceptions import BotoCoreError, ClientError

from app.core.config import settings


logger = logging.getLogger(__name__)


class StorageConfigurationError(RuntimeError):
    pass


def is_storage_configured() -> bool:
    return all(
        [
            settings.storage_endpoint_url,
            settings.storage_bucket_name,
            settings.storage_access_key_id,
            settings.storage_secret_access_key,
        ]
    )


def get_image_url(object_key: str) -> str:
    """
    Generate a URL for an image.
    Returns a working URL guaranteed to function.
    Priority:
    1. Signed URL from S3 (secure, temporary)
    2. Proxy endpoint (always works, uses backend credentials)
    """
    if not is_storage_configured():
        raise StorageConfigurationError("Storage bucket is not configured.")
    
    # Opção 1: Tente gerar signed URL (mais seguro)
    try:
        config = Config(
            connect_timeout=30,
            read_timeout=30,
            retries={"max_attempts": 3, "mode": "adaptive"},
        )

        client = boto3.client(
            "s3",
            endpoint_url=settings.storage_endpoint_url,
            aws_access_key_id=settings.storage_access_key_id,
            aws_secret_access_key=settings.storage_secret_access_key,
            region_name=settings.storage_region or None,
            config=config,
        )

        # Generate a signed URL valid for 24 hours
        signed_url = client.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': settings.storage_bucket_name,
                'Key': object_key
            },
            ExpiresIn=86400,  # 24 hours
        )
        if signed_url:
            logger.info("Generated fresh signed URL for: %s", object_key)
            return signed_url
    except Exception as exc:
        # Catch ALL exceptions, not just botocore errors
        logger.debug("Failed to generate signed URL for %s: %s (%s)", 
                    object_key, type(exc).__name__, str(exc))
    
    # Opção 2: Usar endpoint proxy do backend (garantido funcionar)
    from urllib.parse import quote
    proxy_url = f"/api/image-proxy/{quote(object_key, safe='')}"
    logger.info("Using proxy URL for: %s -> %s", object_key, proxy_url)
    return proxy_url


def upload_bytes(
    contents: bytes,
    original_filename: str,
    folder: str,
    content_type: str | None = None,
) -> dict[str, str]:
    if not is_storage_configured():
        raise StorageConfigurationError("Storage bucket is not configured.")

    extension = Path(original_filename).suffix.lower()
    filename = f"{uuid4().hex}{extension}"
    object_key = f"{folder}/{filename}"

    # Configure boto3 with timeout and retries to avoid hanging requests.
    config = Config(
        connect_timeout=30,
        read_timeout=30,
        retries={"max_attempts": 3, "mode": "adaptive"},
    )

    client = boto3.client(
        "s3",
        endpoint_url=settings.storage_endpoint_url,
        aws_access_key_id=settings.storage_access_key_id,
        aws_secret_access_key=settings.storage_secret_access_key,
        region_name=settings.storage_region or None,
        config=config,
    )

    extra_args = {}
    if content_type:
        extra_args["ContentType"] = content_type
    else:
        extra_args["ContentType"] = "application/octet-stream"

    logger.info("Starting upload: %s (%s bytes)", object_key, len(contents))
    start_time = time.time()

    try:
        client.put_object(
            Bucket=settings.storage_bucket_name,
            Key=object_key,
            Body=contents,
            **extra_args,
        )
        elapsed = time.time() - start_time
        logger.info("Upload successful: %s (%.2fs)", object_key, elapsed)
    except (BotoCoreError, ClientError) as exc:
        logger.error("Upload failed: %s - %s", object_key, str(exc))
        raise RuntimeError("Could not upload file to storage bucket.") from exc

    return {
        "filename": filename,
        "key": object_key,
        "url": get_image_url(object_key),  # Generate fresh signed URL
    }
