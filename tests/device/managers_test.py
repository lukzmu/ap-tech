import threading
import time
from unittest.mock import patch

import pytest
from device.exceptions import MonitorAlreadyRunningError, MonitorIsNotRunningError
from device.managers import DeviceMonitor
from device.repositories import DeviceFileRepository


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

            with pytest.raises(MonitorAlreadyRunningError):
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
            with pytest.raises(MonitorIsNotRunningError):
                device_monitor.stop()

    def test_get_statuses(self, device_monitor, device, device_mapped_reading):
        device_monitor._devices = [device]
        device_monitor._process_readings()

        statuses = device_monitor.get_statuses()

        assert len(statuses) == 1
        assert statuses == {device.id: device_mapped_reading}

    @pytest.mark.parametrize(
        ["file_content", "expected_count"],
        [
            ([{"device_id": 1, "expected_fields": ["current", "voltage"]}], 1),
            (
                [
                    {"device_id": 1, "expected_fields": ["current", "voltage"]},
                    {"device_id": 2, "expected_fields": ["current"]},
                ],
                2,
            ),
            ([{"device_id": 2, "expected_fields": ["current"]}], 1),
        ],
    )
    def test_start_updates_devices(self, device_monitor, device, main_thread_id, file_content, expected_count):
        with (
            patch("threading.get_ident", return_value=main_thread_id),
            patch.object(DeviceFileRepository, "_get_data", return_value=file_content),
        ):
            device_monitor._devices = [device]

            device_monitor.start()
            time.sleep(1)  # Allow time for the worker thread to update the devices

            device_monitor.is_running = False

            assert len(device_monitor._devices) == expected_count
