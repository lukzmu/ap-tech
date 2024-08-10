import threading
from datetime import datetime

from core.exceptions import MainThreadError, TimeIntervalError


def validate_main_thread(thread_id: int) -> None:
    if threading.get_ident() != thread_id:
        raise MainThreadError()


def validate_time_interval(interval: int, last_update: datetime | None) -> None:
    current_time = datetime.now()
    print(current_time)
    if last_update is not None and (current_time - last_update).seconds < interval:
        raise TimeIntervalError
