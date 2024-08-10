import json
import logging
import os
import random
import threading
import time

from device_monitor import Device, DeviceFileRepository, DeviceManager

DEVICES_FILE_PATH = "examples/data/devices.json"
DATA_DIRECTORY_PATH = "examples/data"

# Cleanup between demo runs
if os.path.exists(DATA_DIRECTORY_PATH):
    for file in os.listdir(DATA_DIRECTORY_PATH):
        if file == ".gitkeep":
            continue
        os.remove(f"{DATA_DIRECTORY_PATH}/{file}")

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(threadName)s - %(levelname)s - %(message)s",
)
logging.getLogger().setLevel(logging.INFO)

# Get main thread information
main_thread_id = threading.get_ident()

# Create sample devices
sample_devices = [
    Device(id=1, expected_fields=["current", "voltage"]),
    Device(id=2, expected_fields=["temperature", "humidity"]),
    Device(id=3, expected_fields=["speed", "direction", "altitude"]),
]

# Create a device repository
repository = DeviceFileRepository(
    file_path=DEVICES_FILE_PATH,
    data_location=DATA_DIRECTORY_PATH,
)

# Save sample devices to configuration file
for device in sample_devices:
    repository.add(model=device)

# Show that you can't add new devices with the same id
try:
    repository.add(model=sample_devices[0])
except Exception as e:
    logging.error(e)

# Create a new device manager
device_manager = DeviceManager(
    device_repository=repository,
    main_thread_id=main_thread_id,
)


# Show that you cant run the device manager from a thread other than the main thread
# (Applies to start and stop methods)
def run_start_in_thread():
    try:
        device_manager.start()
    except Exception as e:
        logging.error(e)


threading.Thread(target=run_start_in_thread, name="ExampleThread").start()


# Run the device manager
device_manager.start()

# Wait some time
time.sleep(2)


# Start a thread that will read the device readings every second
def get_readings():
    while device_manager._is_running:  # Private variable, just for demonstration purposes
        readings = device_manager.get_statuses()
        logging.info(f"Readings: {readings}")
        time.sleep(1)


threading.Thread(target=get_readings, name="ReadingThread").start()


# Wait some time, so the manager can update the devices
time.sleep(2)


# Add some readings to the devices
def create_readings():
    for device in sample_devices:
        data_path = f"{DATA_DIRECTORY_PATH}/{device.id}.json"
        device_data = {field: random.randint(0, 1000) for field in device.expected_fields}

        with open(data_path, "w") as file:
            json.dump(device_data, file, indent=4)


create_readings()


# Wait some time to see the outputs
time.sleep(5)

# Update the readings on the go
create_readings()

# Show that you can add a new device at any point
new_device = Device(id=4, expected_fields=["stamina", "charisma", "intelligence"])
repository.add(model=new_device)

# Create some data for the new device
data_path = f"{DATA_DIRECTORY_PATH}/{new_device.id}.json"
new_device_data = {field: random.randint(0, 1000) for field in new_device.expected_fields}
with open(data_path, "w") as file:
    json.dump(new_device_data, file, indent=4)

# Oops, one device disconnected!
os.remove(f"{DATA_DIRECTORY_PATH}/{sample_devices[1].id}.json")

# Wait some time to see the outputs
time.sleep(5)

# Stop the device manager
device_manager.stop()

# Wait some time to see that the thread really stopped
time.sleep(5)
logging.info("End of the demo simulation. Thank you!")
