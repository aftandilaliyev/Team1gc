from abc import ABC, abstractmethod
import io
from typing import Optional

from fastapi import UploadFile


class BaseBucketManager(ABC):
    @abstractmethod
    def get(self, path: str) -> bytes | None:
        pass

    @abstractmethod
    async def get_checksum(self, path: str) -> str | None:
        pass

    @abstractmethod
    async def put(
        self, 
        path: str, 
        file_buffer: io.BytesIO, 
        content_type: Optional[str] = None,
        file_type: Optional[str] = None
    ) -> str:
        pass

    @abstractmethod
    def delete(self, keys: list[str]) -> None:
        pass

    @abstractmethod
    def delete_folder(self, path: str) -> None:
        pass

    @abstractmethod
    def generate_presigned_get_url(self, file_path: str, expiration: int = 3600) -> str | None:
        pass
