import json
import uuid
import aioboto3
from fastapi import UploadFile

from app.core.config import settings


class S3Client:
    def __init__(self) -> None:
        self.session = aioboto3.Session()
        self.bucket_name = settings.S3_BUCKET_NAME

    def _get_client(self):
        return self.session.client(
            service_name="s3",
            endpoint_url=settings.S3_ENDPOINT_URL,
            aws_access_key_id=settings.S3_ACCESS_KEY,
            aws_secret_access_key=settings.S3_SECRET_KEY,
        )

    async def init_bucket(self) -> None:
        async with self._get_client() as client:
            try:
                await client.head_bucket(Bucket=self.bucket_name)
            except Exception:
                await client.create_bucket(Bucket=self.bucket_name)

            policy = {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Sid": "PublicReadGetObject",
                        "Effect": "Allow",
                        "Principal": "*",
                        "Action": ["s3:GetObject"],
                        "Resource": [f"arn:aws:s3:::{self.bucket_name}/*"],
                    }
                ],
            }
            await client.put_bucket_policy(
                Bucket=self.bucket_name,
                Policy=json.dumps(policy),
            )

    async def upload_file(self, file: UploadFile, folder: str = "images") -> tuple[str, str]:
        filename = file.filename or "image.jpg"
        ext = filename.split(".")[-1] if "." in filename else "jpg"
        key = f"{folder}/{uuid.uuid4().hex}.{ext.lower()}"

        content = await file.read()
        content_type = file.content_type or "image/jpeg"

        async with self._get_client() as client:
            try:
                await client.put_object(
                    Bucket=self.bucket_name,
                    Key=key,
                    Body=content,
                    ContentType=content_type,
                )
            except Exception:
                await self.init_bucket()
                await client.put_object(
                    Bucket=self.bucket_name,
                    Key=key,
                    Body=content,
                    ContentType=content_type,
                )

        url = f"{settings.S3_PUBLIC_URL}/{self.bucket_name}/{key}"
        return url, key

    async def delete_file(self, key: str) -> None:
        async with self._get_client() as client:
            await client.delete_object(
                Bucket=self.bucket_name,
                Key=key,
            )


s3_client = S3Client()
