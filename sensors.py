import json
import os
from homebridge import HomebridgeClient


SENSOR_FILE = "/tmp/sensors.json"
# @todo: Maybe this should be configurable
KNOWN_SENSORS = {
        "outdoor": "io:9229676",
        "outdoor2": "io:5041775",
        "sunlight": "io:8548271",
        "thermostat": "somfythermostat:193910495402#1",
        "humidity": "somfythermostat:193910495402#3"
    }


def data(force=False):
    if not force and os.path.exists(SENSOR_FILE):
        with open(SENSOR_FILE, "r") as sensor_file:
            return json.load(sensor_file)

    print("Fetching sensor data...")
    api = HomebridgeClient()
    # array of dictionaries of accessories
    accessory_list = api.accessories()

    # Print accessory information
    for index, item in enumerate(accessory_list):
        print(f"{index:02d}".ljust(4), f"{item['serviceName']} ({item["accessoryInformation"]["Serial Number"]})".rjust(45), "=>", item['uniqueId'])

    print("-" * 36)

    known_sensors = {v: k for k, v in KNOWN_SENSORS.items()}

    sensors_ids_map = {}
    for accessory in accessory_list:
        serial_number = accessory["accessoryInformation"]["Serial Number"]
        if serial_number in known_sensors.keys():
            sensors_ids_map[known_sensors[serial_number]] = accessory["uniqueId"]

    # Write sensor IDs to file
    with open(SENSOR_FILE, "w") as sensor_file:
        json.dump(sensors_ids_map, sensor_file)

    print(json.dumps(sensors_ids_map))

    return sensors_ids_map
