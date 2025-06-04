from abc import ABC, abstractmethod
from typing import Self
class IImageConverter(ABC):
    def convert(self, source_path: str, destination_path: str) -> Self:
        pass