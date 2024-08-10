from typing import Any

import pytest

from device_monitor.device.mappers import DeviceMapper
from device_monitor.device.models import Device


class TestMappers:
    @pytest.fixture
    def device_data(self) -> dict[str, Any]:
        return {
            "device_id": 123,
            "expected_fields": ["current", "voltage"],
        }

    @pytest.fixture
    def expected_serialized_device(self) -> dict[str, Any]:
        def _expected_serialized_device(readings):
            return {
                "device_id": 123,
                "expected_fields": ["current", "voltage"],
                "readings": readings,
            }

        return _expected_serialized_device

    def test_mapper_creates_model(self, device_data):
        device = DeviceMapper.dict_to_model(data=device_data)

        assert device.id == device_data["device_id"]
        assert device.expected_fields == device_data["expected_fields"]
        assert device.readings is None

    @pytest.mark.parametrize(
        ["readings", "expected_readings"],
        [
            (
                {"current": 123, "voltage": 456},
                {"output_current": 123, "output_voltage": 456},
            ),
            (
                {"current": 123, "voltage": 456, "unexpected_reading": 789},
                {"output_current": 123, "output_voltage": 456},
            ),
            (
                {"current": 123},
                {"output_current": 123, "output_voltage": None},
            ),
        ],
    )
    def test_mapper_serializes_model(self, expected_serialized_device, readings, expected_readings):
        device = Device(
            id=123,
            expected_fields=["current", "voltage"],
            readings=readings,
        )

        data = DeviceMapper.model_to_dict(model=device)

        assert data == expected_serialized_device(readings=expected_readings)
