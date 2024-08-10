class DeviceAlreadyExists(Exception):
    def __init__(self, id: int) -> None:
        super().__init__(f"Device with id {id} already exists.")


class ManagerAlreadyRunningError(Exception):
    def __init__(self) -> None:
        super().__init__("Manager is already running.")


class ManagerIsNotRunningError(Exception):
    def __init__(self) -> None:
        super().__init__("Manager is not running.")
