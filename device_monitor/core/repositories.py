from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

from core.mappers import AbstractMapper

ModelType = TypeVar("ModelType")


class DataRepository(ABC, Generic[ModelType]):
    def __init__(self, mapper: AbstractMapper[ModelType]) -> None:
        self._mapper = mapper

    def get(self) -> list[ModelType]:
        data = self._get_data()
        return [self._mapper.dict_to_model(data=item) for item in data]

    @abstractmethod
    def _get_data(self) -> list[dict[str, Any]]:
        pass
