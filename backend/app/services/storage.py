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


def _build_public_url(object_key: str) -> str:
    """
    Build a public URL for the S3 object using the public base URL.
    This ensures URLs are persistent and don't expire.
    """
    if not is_storage_configured():
        raise StorageConfigurationError("Storage bucket is not configured.")
    
    # Use public base URL if configured (preferred - persistent URLs)
    public_base = settings.storage_public_base_url.strip().rstrip("/")
    if public_base:
        url = f"{public_base}/{object_key}"
        logger.info("Generated public URL for: %s", object_key)
        return url
    
    # Fallback to signed URL only if public base URL is not configured
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

    try:
        # Generate a signed URL as fallback (valid for 1 hour)
        signed_url = client.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': settings.storage_bucket_name,
                'Key': object_key
            },
            ExpiresIn=3600,  # 1 hour
        )
        logger.info("Generated signed URL for: %s (fallback)", object_key)
        return signed_url
    except (BotoCoreError, ClientError) as exc:
        logger.error("Failed to generate signed URL: %s - %s", object_key, str(exc))
        raise StorageConfigurationError("Could not generate URL and public_base_url is not configured.") from exc

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
        "url": _build_public_url(object_key),
    }
