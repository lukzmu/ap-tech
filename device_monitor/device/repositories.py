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
        data = []
        if os.path.exists(self._file_path):
            with open(self._file_path) as file:
                data = json.load(file)

        for device in data:
            if device["device_id"] == model.id:
                raise DeviceAlreadyExists(id=model.id)

        device_data = DeviceMapper.model_to_dict(model=model)
        del device_data["readings"]
        data.append(device_data)

        with open(self._file_path, "w") as file:
            json.dump(data, file, indent=4)


class DeviceDataFileRepository(FileRepository[dict[str, Any]]):
    _DATA_MAPPER = None
