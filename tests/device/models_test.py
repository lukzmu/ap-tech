from device.models import Device


class TestModels:
    def test_device_model(self):
        device = Device(
            id=123,
            expected_fields=["current", "voltage"],
            readings={"current": 123, "voltage": 234},
        )

        assert device.id == 123
        assert device.expected_fields == ["current", "voltage"]
        assert device.readings == {"current": 123, "voltage": 234}
