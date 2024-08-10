import pytest

from device_monitor.device.exceptions import DeviceAlreadyExists, MonitorAlreadyRunningError, MonitorIsNotRunningError


class TestExceptions:
    @pytest.mark.parametrize(
        ["exception_class", "message", "parameter"],
        [
            (DeviceAlreadyExists, "Device with id 1 already exists.", 1),
            (MonitorAlreadyRunningError, "Monitor is already running.", None),
            (MonitorIsNotRunningError, "Monitor is not running.", None),
        ],
    )
    def test_exception_messages(self, exception_class, message, parameter):
        with pytest.raises(Exception) as cause:
            assert isinstance(cause, exception_class)
            assert str(cause) == message

            if parameter:
                raise exception_class(parameter)
            else:
                raise exception_class()
