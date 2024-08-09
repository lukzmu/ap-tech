from core.repositories import FileRepository
from device.mappers import DeviceDataMapper, DeviceMapper
from device.models import Device, DeviceData


class DeviceRepository(FileRepository[Device]):
    _DATA_MAPPER = DeviceMapper


class DeviceDataRepository(FileRepository[DeviceData]):
    _DATA_MAPPER = DeviceDataMapper
