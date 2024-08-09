from typing import Any

from core.mappers import AbstractMapper
from core.models import Device, DeviceData


class DeviceMapper(AbstractMapper[Device]):
    @staticmethod
    def dict_to_model(data: dict[str, Any]) -> Device:
        return Device(id=data["device_id"], expected_fields=data["expected_fields"])


class DeviceDataMapper(AbstractMapper[DeviceData]):
    @staticmethod
    def dict_to_model(data: dict[str, Any]) -> DeviceData:
        device_id = data.pop("device_id")
        return DeviceData(device_id=device_id, data=data)

    @staticmethod
    def model_to_dict(model: DeviceData) -> dict[str, Any]:
        return {
            model.device_id: {
                f"output_{key}": value for key, value in model.data.items()
            }
        }
