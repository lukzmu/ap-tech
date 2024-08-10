import logging
import threading
from datetime import datetime
from typing import Any

from core.exceptions import DataFileNotFoundError, EmptyDataError, TimeIntervalError
from core.repositories import DataRepository
from core.validators import validate_main_thread, validate_time_interval
from device.exceptions import ManagerAlreadyRunningError, ManagerIsNotRunningError
from device.mappers import DeviceMapper
from device.models import Device
from device.repositories import DeviceDataFileRepository


class DeviceManager:
    def __init__(
        self,
        device_repository: DataRepository,
        main_thread_id: int,
        update_interval: int = 1,
    ) -> None:
        self._device_repository = device_repository
        self._devices: list[Device] = []

        # Data update settings
        self._update_interval = update_interval
        self._last_update: datetime | None = None

        # Threading settings
        self._worker_thread = None
        self._main_thread_id = main_thread_id
        self._thread_lock = threading.Lock()
        self._is_running = False

    def start(self) -> None:
        validate_main_thread(thread_id=self._main_thread_id)

        if self._is_running:
            raise ManagerAlreadyRunningError

        with self._thread_lock:
            logging.info("Running device manager...")
            self._is_running = True
            self._worker_thread = threading.Thread(target=self._synchronize_data, daemon=True, name="DeviceManager")
            self._worker_thread.start()

    def stop(self) -> None:
        validate_main_thread(thread_id=self._main_thread_id)

        if not self._worker_thread or not self._worker_thread.is_alive():
            raise ManagerIsNotRunningError

        with self._thread_lock:
            logging.info("Stopping device manager...")
            self._is_running = False
            self._worker_thread.join()
            self._worker_thread = None

    def get_statuses(self) -> dict[str, Any]:
        with self._thread_lock:
            return {device.id: DeviceMapper.model_to_dict(model=device)["readings"] for device in self._devices}

    def _synchronize_data(self) -> None:
        while self._is_running:
            try:
                validate_time_interval(interval=self._update_interval, last_update=self._last_update)
                self._update_devices()
                self._process_readings()
            except TimeIntervalError:
                pass

    def _update_devices(self) -> None:
        logging.info("Updating devices...")
        self._devices = self._device_repository.get()

    def _process_readings(self) -> None:
        logging.info("Processing readings...")
        self._last_update = datetime.now()
        for device in self._devices:
            try:
                data_path = f"{self._device_repository.data_location}/{device.id}.json"
                data_repository = DeviceDataFileRepository(file_path=data_path)
                readings = data_repository.get()
                device.readings = readings[-1]
            except (DataFileNotFoundError, EmptyDataError) as cause:
                device.readings = {"error": str(cause)}
