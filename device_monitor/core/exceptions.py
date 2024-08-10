class MainThreadError(Exception):
    def __init__(self) -> None:
        super().__init__("You can run this function from main thread only.")


class TimeIntervalError(Exception):
    def __init__(self) -> None:
        super().__init__("Time interval is not reached yet.")


class DataFileNotFoundError(Exception):
    def __init__(self, file_path: str) -> None:
        super().__init__(f"Data file not found: {file_path}")


class EmptyDataError(Exception):
    def __init__(self) -> None:
        super().__init__("No data.")
