import os
from datetime import datetime
from homebridge import HomebridgeClient
from influxdb_client_3 import InfluxDBClient3, Point
import sensors


# @todo: Maybe there should be Sensor class
def read_data():
    api = HomebridgeClient()

    sensors_uids = sensors.data()
    missing_keys = sensors.KNOWN_SENSORS.keys() - sensors_uids.keys()
    if missing_keys:
        raise KeyError(f"Missing required sensor keys: {missing_keys}")

    indoor = api.sensor_values(sensors_uids["thermostat"])["CurrentTemperature"]
    outdoor = api.sensor_values(sensors_uids["outdoor"])["CurrentTemperature"]
    outdoor2 = api.sensor_values(sensors_uids["outdoor2"])["CurrentTemperature"]
    lux = api.sensor_values(sensors_uids["sunlight"])["CurrentAmbientLightLevel"]
    humidity = api.sensor_values(sensors_uids["humidity"])["CurrentRelativeHumidity"]

    values = {
        "indoor": indoor,
        "outdoor": outdoor,
        "outdoor2": outdoor2,
        "lux": lux,
        "humidity": humidity
    }

    return values


def submit_data(data):
    client = InfluxDBClient3(host=os.getenv("INFLUXDB_URL"),
                             token=os.getenv("INFLUXDB_TOKEN"),
                             org=os.getenv("INFLUXDB_ORG"),
                             database=os.getenv("INFLUXDB_BUCKET"))
    point = Point("somfy")
    for key, value in data.items():
        point.field(key, float(value))

    client.write(point, precision="m")


if __name__ == "__main__":
    data = read_data()
    print(f"{datetime.now()} - Retrieved data: {data}")
    submit_data(data)
