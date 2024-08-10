class DeviceAlreadyExists(Exception):
    def __init__(self, id: int) -> None:
        super().__init__(f"Device with id {id} already exists.")
