from functools import wraps
from threading import Lock
from typing import Any, Callable, TypeVar

T = TypeVar("T")


def thread_safe(lock: Lock) -> Callable[[Callable[..., T]], Callable[..., T]]:
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            with lock:
                return func(*args, **kwargs)

        return wrapper

    return decorator
