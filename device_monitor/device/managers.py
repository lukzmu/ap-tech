import threading
from datetime import datetime
from typing import Any

from core.exceptions import DataFileNotFoundError, NoDataError, TimeIntervalError
from core.repositories import AbstractRepository
from core.validators import validate_main_thread, validate_time_interval
from device.mappers import DeviceMapper
from device.models import Device
from device.repositories import DeviceDataFileRepository


class DeviceManager:
    def __init__(
        self,
        device_repository: AbstractRepository,
        main_thread_id: int,
        update_interval: int = 1,
    ) -> None:
        self._device_repository = device_repository
        self._devices: list[Device] = []

        # Threading settings
        self._main_thread_id = main_thread_id
        self._thread_lock = threading.Lock()
        self._is_running = True

        # Data update settings
        self._update_interval = update_interval
        self._last_update: datetime | None = None

    def start(self) -> None:
        validate_main_thread()
        with self._thread_lock:
            while self._is_running:
                try:
                    validate_time_interval(
                        interval=self._update_interval,
                        last_update=self._last_update,
                    )

                    self._update_devices()
                    self._process_devices()
                except TimeIntervalError:
                    pass

    def stop(self) -> None:
        validate_main_thread()
        with self._thread_lock:
            self._is_running = False

    def get_statuses(self) -> dict[str, Any]:
        with self._thread_lock:
            return {
                device.id: DeviceMapper.model_to_dict(model=device)
                for device in self._devices
            }

    def _update_devices(self) -> None:
        self._devices = self._device_repository.get()

    def _process_devices(self) -> None:
        self._last_update = datetime.now()
        for device in self._devices:
            try:
                data_path = f"{self._device_repository.data_location}/{device.id}.json"
                data_repository = DeviceDataFileRepository(file_path=data_path)
                readings = data_repository.get()
                device.readings = readings[-1]
            except (DataFileNotFoundError, NoDataError) as cause:
                device.readings = {"error": str(cause)}
