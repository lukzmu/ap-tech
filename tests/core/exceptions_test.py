import pytest

from device_monitor.core.exceptions import DataFileNotFoundError, EmptyDataError, MainThreadError, TimeIntervalError


class TestExceptions:
    @pytest.mark.parametrize(
        ["exception_class", "message", "parameter"],
        [
            (MainThreadError, "You can run this function from main thread only.", None),
            (TimeIntervalError, "Time interval is not reached yet.", None),
            (DataFileNotFoundError, "Data file not found: {file_path}", "dummy_path"),
            (EmptyDataError, "No data.", None),
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
