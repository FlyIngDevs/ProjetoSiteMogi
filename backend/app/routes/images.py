"""Public image serving endpoints (proxy from S3 storage)"""
import logging
from typing import Optional
from urllib.parse import unquote

import boto3
from botocore.config import Config
from botocore.exceptions import BotoCoreError, ClientError
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import StreamingResponse

from app.core.config import settings


logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api",
    tags=["images"],
)


@router.get("/image-proxy/{object_key:path}")
async def image_proxy(object_key: str):
    """
    Proxy endpoint to serve images from S3 storage.
    This allows accessing images even when signed URLs fail due to CORS or access issues.
    """
    if not object_key:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No image path provided"
        )
    
    # Decode URL-encoded path
    object_key = unquote(object_key)
    
    # Security: prevent directory traversal
    if ".." in object_key or object_key.startswith("/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid image path"
        )
    
    # Validate that the key is in an allowed folder
    allowed_folders = {"annotators", "carousel", "sponsors", "branding"}
    folder = object_key.split("/")[0] if "/" in object_key else None
    
    if not folder or folder not in allowed_folders:
        logger.warning("Attempted access to unauthorized folder: %s", object_key)
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied to this resource"
        )
    
    # Check storage configuration
    if not all([
        settings.storage_endpoint_url,
        settings.storage_bucket_name,
        settings.storage_access_key_id,
        settings.storage_secret_access_key,
    ]):
        logger.error("Storage not configured")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Storage service not available"
        )
    
    try:
        # Create S3 client
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
        
        # Get the object
        response = client.get_object(
            Bucket=settings.storage_bucket_name,
            Key=object_key
        )
        
        # Extract content type and body
        content_type = response.get('ContentType', 'application/octet-stream')
        body = response['Body'].read()
        
        logger.info("Served image from S3: %s (%d bytes)", object_key, len(body))
        
        # Return as streaming response with appropriate headers
        return StreamingResponse(
            iter([body]),
            media_type=content_type,
            headers={
                "Cache-Control": "public, max-age=3600",  # Cache for 1 hour
                "Content-Length": str(len(body)),
            }
        )
    
    except ClientError as exc:
        error_code = exc.response['Error']['Code']
        if error_code == 'NoSuchKey':
            logger.warning("Image not found in S3: %s", object_key)
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Image not found"
            ) from exc
        elif error_code == 'AccessDenied':
            logger.error("Access denied to S3 object: %s", object_key)
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied"
            ) from exc
        else:
            logger.error("S3 error accessing %s: %s", object_key, str(exc))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to retrieve image"
            ) from exc
    
    except BotoCoreError as exc:
        logger.error("S3 client error: %s", str(exc))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Storage service error"
        ) from exc
    except Exception as exc:
        logger.error("Unexpected error serving image %s: %s", object_key, str(exc))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        ) from exc
