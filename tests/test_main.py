import pytest
from unittest.mock import Mock
from influxdb_client_3 import Point
import main


@pytest.fixture
def mock_sensors(monkeypatch):
    sensors_mock = Mock()
    sensors_mock.data.return_value = {
        "thermostat": "thermostat-uid",
        "outdoor": "outdoor-uid",
        "sunlight": "sunlight-uid",
        "humidity": "humidity-uid"
    }
    monkeypatch.setattr(main, 'sensors', sensors_mock)
    return sensors_mock


@pytest.fixture
def mock_homebridge_client(monkeypatch):
    homebridge_client_mock = Mock()
    homebridge_client_mock_instance = homebridge_client_mock.return_value
    homebridge_client_mock_instance.sensor_values.side_effect = lambda uid: {
        "thermostat-uid": {"CurrentTemperature": 22},
        "outdoor-uid": {"CurrentTemperature": 18},
        "sunlight-uid": {"CurrentAmbientLightLevel": 300},
        "humidity-uid": {"CurrentRelativeHumidity": 45}
    }.get(uid, {})
    monkeypatch.setattr(main, 'HomebridgeClient', homebridge_client_mock)
    return homebridge_client_mock


def test_read_data(mock_sensors, mock_homebridge_client):
    data = main.read_data()
    assert data == {
        "indoor": 22,
        "outdoor": 18,
        "lux": 300,
        "humidity": 45
    }


@pytest.fixture
def mock_influxdb_client(monkeypatch):
    influxdb_client_mock = Mock()
    monkeypatch.setattr(main, 'InfluxDBClient3', influxdb_client_mock)
    return influxdb_client_mock


def test_submit_data(mock_influxdb_client):
    sample_data = {
        "indoor": 22,
        "outdoor": 18,
        "lux": 300,
        "humidity": 45
    }
    main.submit_data(sample_data)
    mock_influxdb_client_instance = mock_influxdb_client.return_value
    mock_influxdb_client_instance.write.assert_called_once()
    point_arg = mock_influxdb_client_instance.write.call_args[0][0]
    assert isinstance(point_arg, Point)
    assert point_arg.to_line_protocol().startswith('somfy')
    for key, value in sample_data.items():
        assert f'{key}={value}' in point_arg.to_line_protocol()
