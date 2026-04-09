from pathlib import Path
from uuid import uuid4

import boto3
from botocore.exceptions import BotoCoreError, ClientError

from app.core.config import settings


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
    public_base = settings.storage_public_base_url.strip().rstrip("/")
    if public_base:
        return f"{public_base}/{object_key}"

    endpoint = settings.storage_endpoint_url.strip().rstrip("/")
    bucket = settings.storage_bucket_name.strip()
    if not endpoint or not bucket:
        raise StorageConfigurationError("Storage public URL is not configured.")

    return f"{endpoint}/{bucket}/{object_key}"


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

    client = boto3.client(
        "s3",
        endpoint_url=settings.storage_endpoint_url,
        aws_access_key_id=settings.storage_access_key_id,
        aws_secret_access_key=settings.storage_secret_access_key,
        region_name=settings.storage_region or None,
    )

    extra_args = {}
    if content_type:
        extra_args["ContentType"] = content_type
    else:
        extra_args["ContentType"] = "application/octet-stream"

    try:
        client.put_object(
            Bucket=settings.storage_bucket_name,
            Key=object_key,
            Body=contents,
            **extra_args,
        )
    except (BotoCoreError, ClientError) as exc:
        raise RuntimeError("Could not upload file to storage bucket.") from exc

    return {
        "filename": filename,
        "key": object_key,
        "url": _build_public_url(object_key),
    }
