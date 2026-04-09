# Railway Deploy Checklist

## Start command

Use the root `Procfile` or set the service start command to:

`cd backend && python run.py`

## Required environment variables

- `DATABASE_URL`
- `SECRET_KEY`
- `UPLOAD_DIR=/app/data/uploads` or another persistent path if you attach a volume

## S3-compatible storage variables

- `STORAGE_ENDPOINT_URL`
- `STORAGE_BUCKET_NAME`
- `STORAGE_ACCESS_KEY_ID`
- `STORAGE_SECRET_ACCESS_KEY`
- `STORAGE_REGION=auto`
- `STORAGE_PUBLIC_BASE_URL`

## Branding and uploads

- The admin uploads images through `/api/admin/upload-image`
- If storage variables are configured, uploads go to the bucket and the returned URL is saved in PostgreSQL
- If storage variables are missing, uploads fall back to local disk

## Health checks after deploy

1. Open `/health`
2. Open `/api`
3. Open `/docs`
4. Open `/api/site-config/branding`
5. Open `/pages/admin.html`
6. Upload a logo in the admin branding section
7. Save an annotator, carousel item, and sponsor with uploaded images

## Notes

- The frontend branding request times out after 8 seconds so the UI should not stay blocked if the API is slow
- `python run.py` fails fast if PostgreSQL is unavailable
