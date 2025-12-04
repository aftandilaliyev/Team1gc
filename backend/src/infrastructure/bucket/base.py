from abc import ABC, abstractmethod

from fastapi import UploadFile


class BaseBucketManager(ABC):
    @abstractmethod
    def get(self, path: str) -> bytes:
        pass

    @abstractmethod
    def get_checksum(self, path: str) -> str:
        pass

    @abstractmethod
    async def put(self, path: str, file: UploadFile) -> tuple[str, int]:
        pass

    @abstractmethod
    def delete(self, urls: list[str]):
        pass

    @abstractmethod
    def delete_folder(self, path: str):
        pass
