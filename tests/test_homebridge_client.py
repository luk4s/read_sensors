import os

import pytest
from unittest.mock import patch, Mock
from homebridge import HomebridgeClient


@pytest.fixture
def mock_env_vars():
    with patch.dict(os.environ, {
        "HOMEBRIDGE_URL": "http://test.url",
        "HOMEBRIDGE_LOGIN": "testuser",
        "HOMEBRIDGE_PASSWORD": "testpass",
        "HOMEBRIDGE_TOKEN": "Bearer testtoken"
    }):
        yield


def test_initialization(mock_env_vars):
    client = HomebridgeClient()
    assert client.url == "http://test.url"
    assert client.username == "testuser"
    assert client.password == "testpass"
    assert client.token == "Bearer testtoken"


def test_check_auth(mock_env_vars):
    client = HomebridgeClient()
    with patch('requests.get') as mock_get:
        mock_get.return_value.status_code = 200
        client.check_auth()
        mock_get.assert_called_once_with("http://test.url/auth/check", headers={"Authorization": "Bearer testtoken"})


def test_login(mock_env_vars):
    client = HomebridgeClient()
    with patch('requests.post') as mock_post:
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "token_type": "Bearer",
            "access_token": "newtoken"
        }
        mock_post.return_value = mock_response
        client.login()
        assert client.token == "Bearer newtoken"
        mock_post.assert_called_once_with(
            "http://test.url/auth/login",
            json={"username": "testuser", "password": "testpass"}
        )


def test_get_accessories(mock_env_vars):
    client = HomebridgeClient()
    with patch.object(HomebridgeClient, 'check_auth', return_value=None) as mock_check_auth:
        with patch('requests.get') as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.json.return_value = {"accessories": []}
            accessories = client.accessories()
            assert accessories == {"accessories": []}
            mock_get.assert_called_once_with("http://test.url/accessories",
                                             headers={"Authorization": "Bearer testtoken"})
            mock_check_auth.assert_called_once()


def test_read_values(mock_env_vars):
    client = HomebridgeClient()
    with patch.object(HomebridgeClient, 'check_auth', return_value=None) as mock_check_auth:
        with patch('requests.get') as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.json.return_value = {"values": {"temperature": 22}}
            values = client.sensor_values("some-uid")
            assert values == {"temperature": 22}
            mock_get.assert_called_once_with("http://test.url/accessories/some-uid",
                                             headers={"Authorization": "Bearer testtoken"})
            mock_check_auth.assert_called_once()
