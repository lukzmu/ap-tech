import threading
from datetime import datetime
from typing import Any

from core.exceptions import MainThreadError
from device.mappers import DeviceMapper
from device.models import Device


class DeviceManager:
    def __init__(self, main_thread_id: int, update_interval: int = 1) -> None:
        self._devices: list[Device] = []

        # Threading settings
        self._main_thread_id = main_thread_id
        self._thread_lock = threading.Lock()
        self._is_running = True

        # Data update settings
        self._update_interval = update_interval
        self._last_update: datetime | None = None

    def start(self) -> None:
        self._validate_main_thread()
        with self._thread_lock:
            while self._is_running:
                if not self._check_time_interval():
                    continue

                self._update_devices()
                self._process_devices()

    def stop(self) -> None:
        self._validate_main_thread()
        with self._thread_lock:
            self._is_running = False

    def get_statuses(self) -> dict[str, Any]:
        with self._thread_lock:
            return {
                device.id: DeviceMapper.model_to_dict(model=device)
                for device in self._devices
            }

    def _validate_main_thread(self) -> None:
        if threading.get_ident() != self._main_thread_id:
            raise MainThreadError

    def _check_time_interval(self) -> bool:
        current_time = datetime.now()
        return (
            self._last_update is None
            or (current_time - self._last_update).seconds >= self._update_interval
        )

    def _update_devices(self) -> None: ...

    def _process_devices(self) -> None: ...
