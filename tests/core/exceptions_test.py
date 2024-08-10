import pytest
from core.exceptions import DataFileNotFoundError, EmptyDataError, MainThreadError, TimeIntervalError


class TestExceptions:
    @pytest.mark.parametrize(
        ["exception_class", "message", "parameter"],
        [
            (MainThreadError, "You can run this function from main thread only.", None),
            (TimeIntervalError, "Time interval is not reached yet.", None),
            (DataFileNotFoundError, "Data file not found: dummy_path", "dummy_path"),
            (EmptyDataError, "No data.", None),
        ],
    )
    def test_exception_messages(self, exception_class, message, parameter):
        with pytest.raises(exception_class) as cause:
            if parameter:
                raise exception_class(parameter)
            else:
                raise exception_class()

        assert str(cause.value) == message
