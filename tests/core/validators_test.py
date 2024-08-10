from datetime import datetime
from unittest.mock import patch

import pytest

from device_monitor.core.exceptions import MainThreadError, TimeIntervalError
from device_monitor.core.validators import validate_main_thread, validate_time_interval


class TestValidators:
    def test_validate_incorrect_main_thread(self, main_thread_id):
        with patch("threading.get_ident") as mock_thread:
            mock_thread.return_value = main_thread_id

            with pytest.raises(Exception) as cause:
                assert isinstance(cause, MainThreadError)
                validate_main_thread(thread_id=main_thread_id + 1)

    def test_validate_correct_main_thread(self, main_thread_id):
        with patch("threading.get_ident") as mock_thread:
            mock_thread.return_value = main_thread_id
            validate_main_thread(thread_id=main_thread_id)

    @pytest.mark.parametrize(
        ["interval", "last_update", "should_raise"],
        [
            (10, None, False),
            (10, "2024-08-10 10:00:11", False),
            (10, "2024-08-10 10:00:10", True),
            (10, "2024-08-10 09:59:59", True),
        ],
    )
    @pytest.mark.freezetime("2024-08-10 10:00:00")
    def test_validate_time_interval(self, freezer, interval, last_update, should_raise):
        update_time = datetime.strptime(last_update, "%Y-%m-%d %H:%M:%S") if last_update else None

        if should_raise:
            with pytest.raises(Exception) as cause:
                assert isinstance(cause, TimeIntervalError)
                validate_time_interval(interval, update_time)
        else:
            validate_time_interval(interval, update_time)
