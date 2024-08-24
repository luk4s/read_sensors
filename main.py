import os
from datetime import datetime
from homebridge import HomebridgeClient
from influxdb_client_3 import InfluxDBClient3, Point
import sensors


def read_data():
    api = HomebridgeClient()

    sensors_uids = sensors.data()
    indoor = api.sensor_values(sensors_uids["thermostat"])["CurrentTemperature"]
    outdoor = api.sensor_values(sensors_uids["outdoor"])["CurrentTemperature"]
    lux = api.sensor_values(sensors_uids["sunlight"])["CurrentAmbientLightLevel"]
    humidity = api.sensor_values(sensors_uids["humidity"])["CurrentRelativeHumidity"]

    data = {
        "indoor": indoor,
        "outdoor": outdoor,
        "lux": lux,
        "humidity": humidity
    }
    return data


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
