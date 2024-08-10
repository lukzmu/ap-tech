import json
from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

from core.exceptions import DataFileNotFoundError, EmptyDataError
from core.mappers import AbstractMapper

ModelType = TypeVar("ModelType")


class DataRepository(ABC, Generic[ModelType]):
    _DATA_MAPPER: AbstractMapper[ModelType] | None

    def get(self) -> list[ModelType] | list[dict[str, Any]]:
        data = self._get_data()
        if self._DATA_MAPPER:
            return [self._DATA_MAPPER().dict_to_model(data=item) for item in data]
        return data

    @abstractmethod
    def _get_data(self) -> list[dict[str, Any]]:
        pass


class FileRepository(DataRepository[ModelType]):
    def __init__(self, file_path: str) -> None:
        self._file_path = file_path

    def _get_data(self) -> list[dict[str, Any]]:
        try:
            with open(self._file_path) as file:
                data = json.load(file)
                if not data:
                    raise EmptyDataError
                return data

        except FileNotFoundError as cause:
            raise DataFileNotFoundError(file_path=self._file_path) from cause
