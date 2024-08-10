import json

import pytest
from device.exceptions import DeviceAlreadyExists
from device.models import Device


class TestDeviceFileRepository:
    def test_add_new_device(self, device_file_repository, device):
        with open(device_file_repository._file_path) as file:
            original_data = json.load(file)

        new_device = Device(id=2, expected_fields=["current", "voltage"])
        device_file_repository.add(new_device)

        with open(device_file_repository._file_path) as file:
            data = json.load(file)

        assert len(data) == 2
        assert data[1]["device_id"] == new_device.id
        assert data[1]["expected_fields"] == new_device.expected_fields
        assert "readings" not in data[1]

        # Cleanup after test
        with open(device_file_repository._file_path, "w") as file:
            json.dump(original_data, file)

    def test_add_existing_device(self, device_file_repository, device):
        with pytest.raises(DeviceAlreadyExists):
            device_file_repository.add(device)

    def test_get_devices(self, device_file_repository, device):
        devices = device_file_repository.get()

        assert len(devices) == 1
        assert devices[0].id == device.id
        assert devices[0].expected_fields == device.expected_fields


class TestDeviceDataFileRepository:
    def get_device_data(self, device_data_file_repository, device_reading):
        data = device_data_file_repository.get()

        assert len(data) == 1
        assert data[0] == device_reading[0]
