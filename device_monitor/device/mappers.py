from typing import Any

from core.mappers import AbstractMapper
from device.models import Device


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
            "device_id": model.id,
            "expected_fields": model.expected_fields,
            "readings": (
                model.readings
                if model.readings and "error" in model.readings
                else {
                    f"output_{reading_name}": model.readings.get(reading_name) for reading_name in model.expected_fields
                }
                if model.readings
                else None
            ),
        }
