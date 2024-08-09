from dataclasses import dataclass


@dataclass(frozen=True)
class Device:
    id: int
    expected_fields: list[str]


@dataclass(frozen=True)
class DeviceData:
    device_id: int
    data: dict[str, str | int | bool | float]
