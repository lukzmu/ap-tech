from typing import Any

from core.mappers import AbstractMapper
from core.models import Device


class DeviceMapper(AbstractMapper[Device]):
    @staticmethod
    def dict_to_model(data: dict[str, Any]) -> Device:
        return Device(
            id=data["device_id"],
            expected_fields=data["expected_fields"],
        )

    @staticmethod
    def model_to_dict(model: Device) -> dict[str, Any]:
        return {
            f"output_{reading_name}": reading_value
            for reading_name, reading_value in model.readings.items()
            if reading_name in model.expected_fields
        }
