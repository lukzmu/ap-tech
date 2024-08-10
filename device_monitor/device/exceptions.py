class DeviceAlreadyExists(Exception):
    def __init__(self, id: int) -> None:
        super().__init__(f"Device with id {id} already exists.")


class MonitorAlreadyRunningError(Exception):
    def __init__(self) -> None:
        super().__init__("Monitor is already running.")


class MonitorIsNotRunningError(Exception):
    def __init__(self) -> None:
        super().__init__("Monitor is not running.")
