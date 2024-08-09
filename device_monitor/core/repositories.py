import json
from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

from core.mappers import AbstractMapper

ModelType = TypeVar("ModelType")


class DataRepository(ABC, Generic[ModelType]):
    _DATA_MAPPER: AbstractMapper[ModelType]

    def get(self) -> list[ModelType]:
        data = self._get_data()
        return [self._DATA_MAPPER().dict_to_model(data=item) for item in data]

    @abstractmethod
    def _get_data(self) -> list[dict[str, Any]]:
        pass


class FileRepository(DataRepository[ModelType]):
    def __init__(self, file_path: str) -> None:
        self._file_path = file_path

    def _get_data(self) -> list[dict[str, Any]]:
        with open(self._file_path) as file:
            return json.load(file)
