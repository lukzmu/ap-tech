import threading

import pytest

from device_monitor.core.exceptions import MainThreadError
from device_monitor.core.validators import validate_main_thread


class TestValidators:
    def test_validate_incorrect_main_thread(self):
        with pytest.raises(Exception) as cause:
            assert isinstance(cause, MainThreadError)
            validate_main_thread(thread_id=12345)

    def test_validate_correct_main_thread(self):
        main_thread_id = threading.get_ident()
        validate_main_thread(thread_id=main_thread_id)
