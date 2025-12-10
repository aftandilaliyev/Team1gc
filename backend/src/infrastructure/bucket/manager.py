import io

import boto3
from botocore.exceptions import ClientError
from loguru import logger

from src.infrastructure.bucket.base import BaseBucketManager
from src.shared.exceptions import FileUploadError, PresignedUrlError, FileDeleteError
from src.shared.utils.bucket import generate_unique_filepath, get_public_url
from src.shared.config import settings


class R2BucketManager(BaseBucketManager):
    _client: boto3.Session

    def __init__(self):
        super().__init__()
        self._client = boto3.client(
            service_name='s3',
            endpoint_url=settings.R2_ENDPOINT_URL,
            aws_access_key_id=settings.R2_ACCESS_KEY_ID.get_secret_value(),
            aws_secret_access_key=settings.R2_SECRET_ACCESS_KEY.get_secret_value(),
            region_name='auto')

    def get(
            self,
            file_path: str
    ) -> bytes | None:
        try:
            response = self._client.get_object(
                Bucket=settings.R2_BUCKET_NAME,
                Key=file_path,
            )
            return response["Body"].read()
        except self._client.exceptions.NoSuchKey:
            return None
        except Exception as e:
            raise FileUploadError(
                f"Error getting file from R2: {e}")

    async def get_checksum(self, path: str) -> str:
        try:
            response = self._client.head_object(
                Bucket=settings.R2_BUCKET_NAME,
                Key=path,
            )
            return response["ETag"]
        except self._client.exceptions.NoSuchKey:
            return None
        except Exception as e:
            raise FileUploadError(
                f"Error getting file checksum from R2: {e}")

    async def put(
            self,
            path: str,
            file_buffer: io.BytesIO,
            content_type: str | None = None,
            file_type: str | None = None,
    ) -> str:
        """
        Uploads a file to R2 storage.
        :param path: The path where the file will be stored.
        :param file: The file to be uploaded.
        :param file_type: The type of the file (e.g., image/png).
        :return: The unique key of the uploaded file.
        """
        try:
            unique_key = generate_unique_filepath(path, file_type)
            self._client.upload_fileobj(
                file_buffer,
                Bucket=settings.R2_BUCKET_NAME,
                Key=unique_key,
                ExtraArgs={
                    "ContentType": content_type
                }
            )
            return unique_key
        except Exception as e:
            raise FileUploadError(
                f"Error uploading file to R2: {e}")

    def delete(
            self,
            keys: list[str]
    ) -> None:
        if keys:
            delete_keys = [{"Key": key} for key in keys]
            for i in range(0, len(delete_keys), 1000):
                batch = delete_keys[i:i + 1000]
                try:
                    self._client.delete_objects(
                        Bucket=settings.R2_BUCKET_NAME,
                        Delete={"Objects": batch}
                    )
                except ClientError as e:
                    raise FileDeleteError(
                        f"Error deleting objects from R2: {e}")
                except Exception as e:
                    raise FileDeleteError(
                        f"Unexpected error deleting objects from R2: {e}")

    def delete_folder(
            self,
            folder_prefix: str
    ) -> None:
        if not folder_prefix.endswith("/"):
            folder_prefix += "/"

        objects_to_delete = []
        try:
            paginator = self._client.get_paginator('list_objects_v2')
            pages = paginator.paginate(
                Bucket=settings.R2_BUCKET_NAME, Prefix=folder_prefix)

            for page in pages:
                if "Contents" in page:
                    for obj in page["Contents"]:
                        objects_to_delete.append({"Key": obj["Key"]})

            if objects_to_delete:
                self.delete([obj["Key"] for obj in objects_to_delete])

        except ClientError as e:
            raise FileDeleteError(
                f"Error listing or deleting folder contents from R2: {e}")
        except Exception as e:
            raise FileDeleteError(
                f"Unexpected error deleting folder from R2: {e}")

    def generate_presigned_get_url(
            self,
            file_path: str,
            expiration: int = 3600  # Default to 1 hour
    ) -> str | None:
        try:
            return self._client.generate_presigned_url(
                'get_object',
                Params={'Bucket': settings.R2_BUCKET_NAME, 'Key': file_path},
                ExpiresIn=expiration,
                HttpMethod='GET'
            )
        except ClientError as e:
            logger.error(
                "Error generating presigned URL for {}: {}", file_path, e)
            return None
        except Exception as e:
            raise PresignedUrlError(
                f"Unexpected error generating presigned URL: {e}")

    def get_public_url(self, file_key: str) -> str:
        """
        Get the public URL for a file stored in R2.
        
        Args:
            file_key: The key/path of the file in the bucket
            
        Returns:
            Public URL for the file
        """
        return get_public_url(file_key, settings.R2_PUBLIC_DOMAIN)
