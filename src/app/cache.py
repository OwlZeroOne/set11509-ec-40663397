import json
import os
from datetime import datetime, timedelta
from typing import Any

CACHE_FILE = "cache.json"


class CacheSingleton:
    __instance = None
    __user = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def save(self, user: dict, token: str) -> None:
        data = {
            "uid": user["uid"],
            "name": user["name"],
            "username": user["username"],
            "email": user["email"],
            "role": user["role"],
            "tickers": user["tickers"],
            "sectors": user["sectors"],
            "threshold": user["threshold"],
            "token": token,
            "expiry": str(datetime.now() + timedelta(hours=1)),
        }
        with open(CACHE_FILE, "w") as f:
            json.dump(data, f)

    def load(self) -> None:
        if os.path.exists(CACHE_FILE):
            with open(CACHE_FILE, "r") as f:
                data = json.load(f)
                tickers = data["tickers"]
                sectors = data["sectors"]

                if sectors:
                    if isinstance(sectors, str):
                        sectors = sectors.split(",")
                else:
                    sectors = []

                if tickers:
                    if isinstance(tickers, str):
                        tickers = tickers.split(",")
                else:
                    tickers = []

                self.__user = {
                    "uid": data["uid"],
                    "name": data["name"],
                    "username": data["username"],
                    "email": data["email"],
                    "role": data["role"],
                    "threshold": data["threshold"],
                    "tickers": tickers,
                    "sectors": sectors,
                    "token": data["token"],
                    "expiry": data["expiry"]
                }

    def is_valid(self) -> bool:
        if self.__user is None:
            return False
        expiry = datetime.fromisoformat(self.__user["expiry"])
        return datetime.now() < expiry

    def clear(self) -> None:
        if os.path.exists(CACHE_FILE):
            os.remove(CACHE_FILE)
            self.__user = None

    def get_token(self) -> str | None:
        if self.__user is None:
            return None
        return self.__user["token"]

    def get(self, prop: str | None = None) -> dict | None:
        if self.__user is not None:
            if prop is None:
                return self.__user
            return self.__user[prop]
        return None

    def update_cache_property(self, prop: str, new_value: Any) -> None:
        if self.__user is not None:
            self.__user[prop] = new_value
        self.save(self.__user, self.get_token())