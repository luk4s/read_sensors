import os
import requests


# API client for Homebridge
class HomebridgeClient:
    def __init__(self):
        self.url = os.getenv("HOMEBRIDGE_URL")
        self.username = os.getenv("HOMEBRIDGE_LOGIN")
        self.password = os.getenv("HOMEBRIDGE_PASSWORD")
        self.token = os.getenv("HOMEBRIDGE_TOKEN")

    def headers(self):
        return {"Authorization": self.token}

    def check_auth(self):
        response = requests.get(f"{self.url}/auth/check", headers=self.headers())
        if response.status_code == 401:
            self.login()

    def login(self):
        response = requests.post(
            f"{self.url}/auth/login",
            json={"username": self.username, "password": self.password}
        )
        if response.status_code == 201:
            json_body = response.json()
            self.token = f"{json_body['token_type']} {json_body['access_token']}"
            os.putenv("HOMEBRIDGE_TOKEN", self.token)

    def accessories(self):
        self.check_auth()
        response = requests.get(f"{self.url}/accessories", headers=self.headers())
        return response.json()

    def sensor_values(self, uid):
        self.check_auth()
        response = requests.get(f"{self.url}/accessories/{uid}", headers=self.headers())
        if response.status_code != 200:
            raise Exception("Connection ERROR!")
        return response.json()["values"]
