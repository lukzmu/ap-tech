import pytest
from device.exceptions import DeviceAlreadyExists, MonitorAlreadyRunningError, MonitorIsNotRunningError


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
        with pytest.raises(exception_class) as cause:
            if parameter:
                raise exception_class(parameter)
            else:
                raise exception_class()

        assert str(cause.value) == message
