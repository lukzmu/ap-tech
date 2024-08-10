import json
from typing import Any

from core.repositories import FileRepository
from device.mappers import DeviceMapper
from device.models import Device


class DeviceFileRepository(FileRepository[Device]):
    _DATA_MAPPER = DeviceMapper

    def __init__(self, file_path: str, data_location: str) -> None:
        super().__init__(file_path)
        self.data_location = data_location

    def add(self, model: Device) -> None:
        with open(self._file_path, "a") as file:
            data = json.load(file)
            device_data = DeviceMapper.model_to_dict(model=model)
            del device_data["readings"]
            data.append(device_data)
            json.dump(data, file)


class DeviceDataFileRepository(FileRepository[dict[str, Any]]):
    _DATA_MAPPER = None
