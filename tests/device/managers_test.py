import threading
import time
from unittest.mock import patch

import pytest

from device_monitor.device.exceptions import MonitorAlreadyRunningError, MonitorIsNotRunningError
from device_monitor.device.managers import DeviceMonitor


class TestDeviceMonitor:
    @pytest.fixture
    def device_monitor(self, device_file_repository, main_thread_id):
        return DeviceMonitor(device_repository=device_file_repository, main_thread_id=main_thread_id)

    def test_start_monitor_success(self, device_monitor, main_thread_id):
        with (
            patch("threading.get_ident") as mock_thread,
            patch.object(threading.Thread, "start") as mock_start,
        ):
            mock_thread.return_value = main_thread_id

            device_monitor.start()

            assert device_monitor._is_running is True
            assert device_monitor._worker_thread is not None
            mock_start.assert_called_once()

    def test_start_monitor_already_running(self, device_monitor, main_thread_id):
        with patch("threading.get_ident") as mock_thread:
            mock_thread.return_value = main_thread_id
            device_monitor._is_running = True

            with pytest.raises(Exception) as cause:
                assert isinstance(cause, MonitorAlreadyRunningError)
                device_monitor.start()

    def test_stop_monitor_success(self, device_monitor, main_thread_id):
        with (
            patch("threading.get_ident") as mock_thread,
            patch.object(threading.Thread, "is_alive") as mock_is_alive,
            patch.object(threading.Thread, "join") as mock_join,
        ):
            mock_thread.return_value = main_thread_id
            mock_is_alive.return_value = True
            device_monitor._is_running = True
            device_monitor._worker_thread = threading.Thread(target=lambda: time.sleep(1))

            device_monitor.stop()

            assert device_monitor._is_running is False
            assert device_monitor._worker_thread is None
            mock_is_alive.assert_called_once()
            mock_join.assert_called_once()

    def test_stop_monitor_not_running(self, device_monitor, main_thread_id):
        with patch("threading.get_ident") as mock_thread:
            mock_thread.return_value = main_thread_id
            with pytest.raises(Exception) as cause:
                assert isinstance(cause, MonitorIsNotRunningError)
                device_monitor.stop()

    def test_get_statuses(self, device_monitor, device, device_mapped_reading):
        device_monitor._devices = [device]
        device_monitor._process_readings()

        statuses = device_monitor.get_statuses()

        assert len(statuses) == 1
        assert statuses == {device.id: device_mapped_reading}
