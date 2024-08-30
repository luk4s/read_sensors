import os
import pytest
import json
import os
from unittest.mock import patch, Mock
from homebridge import HomebridgeClient
import sensors


@pytest.fixture
def mock_env_vars():
    with patch.dict(os.environ, {
        "HOMEBRIDGE_URL": "http://test.url",
        "HOMEBRIDGE_LOGIN": "testuser",
        "HOMEBRIDGE_PASSWORD": "testpass",
        "HOMEBRIDGE_TOKEN": "Bearer testtoken"
    }):
        yield


@pytest.fixture(autouse=True)
def clear_sensors_file_fixture():
    if os.path.exists(sensors.SENSOR_FILE):
        os.remove(sensors.SENSOR_FILE)
    yield
    os.remove(sensors.SENSOR_FILE)

# define mock_sensor_data
mock_sensor_data = [
    {"serviceName": "Thermostat", "uniqueId": "thermostat-uid", "type": "Thermostat", "accessoryInformation": {"Serial Number": "somfythermostat:193910495402#1"}},
    {"serviceName": "LightSensor", "uniqueId": "light-uid", "type": "LightSensor", "accessoryInformation": {"Serial Number": "io:8548271"}},
    {"serviceName": "TemperatureSensor", "uniqueId": "temp-uid", "type": "TemperatureSensor", "accessoryInformation": {"Serial Number": "io:9229676"}},
    {"serviceName": "TemperatureSenso2r", "uniqueId": "temp2-uid", "type": "TemperatureSensor", "accessoryInformation": {"Serial Number": "io:5041775"}},
    {"serviceName": "HumiditySensor", "uniqueId": "humidity-uid", "type": "HumiditySensor", "accessoryInformation": {"Serial Number": "somfythermostat:193910495402#3"}}
]


def test_filter_and_organize_sensor_data(mock_env_vars, tmp_path):
    with patch.object(HomebridgeClient, 'accessories', return_value=mock_sensor_data):
        data = sensors.data()
        assert data == {
            "outdoor": "temp-uid",
            "outdoor2": "temp2-uid",
            "sunlight": "light-uid",
            "thermostat": "thermostat-uid",
            "humidity": "humidity-uid"
        }


def test_write_sensor_data_to_file(mock_env_vars, tmp_path):
    with patch.object(HomebridgeClient, 'accessories', return_value=mock_sensor_data):
        data = sensors.data()
        sensor_file_path = tmp_path / "sensors.json"
        with open(sensor_file_path, "w") as sensor_file:
            json.dump(data, sensor_file)
        with open(sensor_file_path, "r") as sensor_file:
            written_data = json.load(sensor_file)
        assert written_data == data
