import json
import os
from homebridge import HomebridgeClient


SENSOR_FILE = "/tmp/sensors.json"


def data():
    if os.path.exists(SENSOR_FILE):
        with open(SENSOR_FILE, "r") as sensor_file:
            return json.load(sensor_file)

    print("Fetching sensor data...")
    api = HomebridgeClient()
    # array of dictionaries of accessories
    accessory_list = api.accessories()

    # Print accessory information
    for index, item in enumerate(accessory_list):
        print(f"{index:02d}".ljust(4), f"{item['serviceName']}".rjust(25), "=>", item['uniqueId'])

    print("-" * 36)

    # Filter and organize sensor data
    sensor_types = ["Thermostat", "LightSensor", "TemperatureSensor", "HumiditySensor"]
    sensors_list = {item['type']: item for item in accessory_list if item['type'] in sensor_types}

    sensors_ids_map = {
        "outdoor": sensors_list.get("TemperatureSensor", {}).get("uniqueId"),
        "sunlight": sensors_list.get("LightSensor", {}).get("uniqueId"),
        "thermostat": sensors_list.get("Thermostat", {}).get("uniqueId"),
        "humidity": sensors_list.get("HumiditySensor", {}).get("uniqueId")
    }
    # Write sensor IDs to file
    with open(SENSOR_FILE, "w") as sensor_file:
        json.dump(sensors_ids_map, sensor_file)

    print(json.dumps(sensors_ids_map))

    return sensors_ids_map
