import pytest
from device.models import Device
from device.repositories import DeviceDataFileRepository, DeviceFileRepository


@pytest.fixture
def device_file_repository():
    file_path = "tests/data/devices.json"
    data_location = "tests/data"
    return DeviceFileRepository(file_path=file_path, data_location=data_location)


@pytest.fixture
def device_data_file_repository():
    file_path = "data/1.json"
    return DeviceDataFileRepository(file_path=file_path)


@pytest.fixture
def device():
    return Device(id=1, expected_fields=["current", "voltage"])


@pytest.fixture
def device_reading():
    return {"current": 42, "voltage": 220}


@pytest.fixture
def device_mapped_reading():
    return {"output_current": 42, "output_voltage": 220}
