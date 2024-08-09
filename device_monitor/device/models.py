from dataclasses import dataclass


@dataclass(frozen=True)
class Device:
    id: int
    expected_fields: list[str]
    readings: dict[str, str | int | bool | float | None] | None = None
