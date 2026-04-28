from pathlib import Path
from urllib.parse import quote
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
    """Check if all required storage configuration is present."""
    return all([
        settings.storage_endpoint_url,
        settings.storage_bucket_name,
        settings.storage_access_key_id,
        settings.storage_secret_access_key,
    ])


def get_image_url(object_key: str) -> str:
    """
    Generate a permanent URL for an image using proxy endpoint.
    
    The proxy endpoint uses backend credentials to access S3,
    so the URL never expires (unlike signed URLs which expire after 24h).
    
    Args:
        object_key: The S3 object key (e.g., "carousel/abc123.jpg")
    
    Returns:
        A permanent proxy URL that never expires
    
    Raises:
        StorageConfigurationError: If storage is not configured
    """
    if not is_storage_configured():
        raise StorageConfigurationError("Storage bucket is not configured.")
    
    # Always use proxy endpoint - never expires
    proxy_url = f"/api/image-proxy/{quote(object_key, safe='')}"
    logger.info("Generated permanent proxy URL for: %s", object_key)
    return proxy_url


def _create_s3_client() -> boto3.client:
    """Create and configure an S3 client with retry logic."""
    config = Config(
        connect_timeout=30,
        read_timeout=30,
        retries={"max_attempts": 3, "mode": "adaptive"},
    )
    
    return boto3.client(
        "s3",
        endpoint_url=settings.storage_endpoint_url,
        aws_access_key_id=settings.storage_access_key_id,
        aws_secret_access_key=settings.storage_secret_access_key,
        region_name=settings.storage_region or None,
        config=config,
    )


def upload_bytes(
    contents: bytes,
    original_filename: str,
    folder: str,
    content_type: str | None = None,
) -> dict[str, str]:
    """
    Upload file bytes to S3 storage.
    
    Args:
        contents: File contents as bytes
        original_filename: Original filename (used to extract extension)
        folder: S3 folder/prefix (e.g., "carousel", "annotators")
        content_type: MIME type (auto-detected if not provided)
    
    Returns:
        Dictionary with filename, key, and permanent URL
    
    Raises:
        StorageConfigurationError: If storage is not configured
        RuntimeError: If upload fails
    """
    # Validate storage configuration
    if not is_storage_configured():
        missing = []
        if not settings.storage_endpoint_url:
            missing.append("STORAGE_ENDPOINT_URL")
        if not settings.storage_bucket_name:
            missing.append("STORAGE_BUCKET_NAME")
        if not settings.storage_access_key_id:
            missing.append("STORAGE_ACCESS_KEY_ID")
        if not settings.storage_secret_access_key:
            missing.append("STORAGE_SECRET_ACCESS_KEY")
        
        raise StorageConfigurationError(
            f"Storage bucket not configured. Missing: {', '.join(missing)}"
        )
    
    # Generate unique filename
    extension = Path(original_filename).suffix.lower()
    filename = f"{uuid4().hex}{extension}"
    object_key = f"{folder}/{filename}"
    
    # Prepare upload arguments
    extra_args = {
        "ContentType": content_type or "application/octet-stream"
    }
    
    logger.info("Starting upload: %s (%s bytes)", object_key, len(contents))
    start_time = time.time()
    
    try:
        # Upload to S3
        client = _create_s3_client()
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
        "url": get_image_url(object_key),
    }