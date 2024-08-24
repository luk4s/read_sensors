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


def test_filter_and_organize_sensor_data(mock_env_vars, tmp_path):
    with patch.object(HomebridgeClient, 'accessories', return_value=[
        {"serviceName": "Thermostat", "uniqueId": "thermostat-uid", "type": "Thermostat"},
        {"serviceName": "LightSensor", "uniqueId": "light-uid", "type": "LightSensor"},
        {"serviceName": "TemperatureSensor", "uniqueId": "temp-uid", "type": "TemperatureSensor"},
        {"serviceName": "HumiditySensor", "uniqueId": "humidity-uid", "type": "HumiditySensor"}
    ]):
        data = sensors.data()
        assert data == {
            "outdoor": "temp-uid",
            "sunlight": "light-uid",
            "thermostat": "thermostat-uid",
            "humidity": "humidity-uid"
        }


def test_write_sensor_data_to_file(mock_env_vars, tmp_path):
    with patch.object(HomebridgeClient, 'accessories', return_value=[
        {"serviceName": "Thermostat", "uniqueId": "thermostat-uid", "type": "Thermostat"},
        {"serviceName": "LightSensor", "uniqueId": "light-uid", "type": "LightSensor"},
        {"serviceName": "TemperatureSensor", "uniqueId": "temp-uid", "type": "TemperatureSensor"},
        {"serviceName": "HumiditySensor", "uniqueId": "humidity-uid", "type": "HumiditySensor"}
    ]):
        data = sensors.data()
        sensor_file_path = tmp_path / "sensors.json"
        with open(sensor_file_path, "w") as sensor_file:
            json.dump(data, sensor_file)
        with open(sensor_file_path, "r") as sensor_file:
            written_data = json.load(sensor_file)
        assert written_data == data
