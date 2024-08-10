from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

ModelType = TypeVar("ModelType")


class AbstractMapper(ABC, Generic[ModelType]):
    @staticmethod
    @abstractmethod
    def dict_to_model(data: dict[str, Any]) -> ModelType:
        pass  # pragma: no cover

    @staticmethod
    @abstractmethod
    def model_to_dict(model: ModelType) -> dict[str, Any]:
        pass  # pragma: no cover
