import json

import pytest

from device_monitor.device.exceptions import DeviceAlreadyExists
from device_monitor.device.models import Device
from device_monitor.device.repositories import DeviceDataFileRepository, DeviceFileRepository


class TestDeviceFileRepository:
    @pytest.fixture
    def sample_device(self):
        return Device(id="device1", expected_fields=["current", "voltage"])

    @pytest.fixture
    def device_file_repository(self):
        def _device_file_repository(path):
            file_path = f"{path}/devices.json"
            data_location = "data"
            return DeviceFileRepository(file_path=file_path, data_location=data_location)

        return _device_file_repository

    def test_add_new_device(self, device_file_repository, sample_device):
        device_file_repository.add(sample_device)

        with open(device_file_repository._file_path) as file:
            data = json.load(file)

        assert len(data) == 1
        assert data[0]["device_id"] == sample_device.id
        assert data[0]["expected_fields"] == sample_device.expected_fields
        assert "readings" not in data[0]

    def test_add_existing_device(self, device_file_repository, sample_device):
        device_file_repository.add(sample_device)

        with pytest.raises(DeviceAlreadyExists):
            device_file_repository.add(sample_device)

    def test_get_devices(self, device_file_repository, sample_device):
        device_file_repository.add(sample_device)
        devices = device_file_repository.get_all()

        assert len(devices) == 1
        assert isinstance(devices[0], Device)
        assert devices[0].id == sample_device.id
        assert devices[0].expected_fields == sample_device.expected_fields


class TestDeviceDataFileRepository:
    @pytest.fixture
    def expected_data(self):
        return [
            {"current": 123, "voltage": 234},
        ]

    @pytest.fixture
    def device_data_file_repository(self):
        def _device_data_file_repository(path):
            file_path = f"{path}/device_data.json"
            return DeviceDataFileRepository(file_path=file_path)

        return _device_data_file_repository

    def get_device_data(self, device_data_file_repository, expected_data):
        with open(device_data_file_repository._file_path, "w") as file:
            data = json.dump(expected_data, file)

        data = device_data_file_repository.get_all()

        assert len(data) == 1
        assert data[0] == expected_data[0]
