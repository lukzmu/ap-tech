class MainThreadError(Exception):
    def __init__(self) -> None:
        super().__init__("You can run this function from main thread only.")


class TimeIntervalError(Exception):
    def __init__(self) -> None:
        super().__init__("Time interval is not reached yet.")
