import pandas as pd
import requests
from requests import Response

BASE_URL = "http://localhost:5010/gateway"

SHARES_URL = f"{BASE_URL}/shares"
BROKERS_URL = f"{BASE_URL}/brokers"


USER_DB_FIELDS = {"name", "username", "email", "password_hash", "role", "tickers", "sectors"}


def login_user(username: str, password: str) -> Response:
    return requests.post(
        f"{BASE_URL}/login",
        json={"username": username, "password": password}
    )


def register_user(username: str, password: str, email: str, name: str, role: str) -> int:
    return requests.post(
        f"{BASE_URL}/register",
        json={
            "username": username,
            "password": password,
            "email": email,
            "name": name,
            "role": role
        }
    ).status_code


def get_all_users(token) -> Response:
    return requests.get(
        f"{BASE_URL}/users/get-all-users",
        headers={"Authorization": f"Bearer {token}"}
    )


def update_user(user: dict, token: str) -> int:
    attributes = {k: v for k, v in user.items() if k in USER_DB_FIELDS}
    if "tickers" in attributes and isinstance(attributes["tickers"], list):
        attributes["tickers"] = ",".join(attributes["tickers"])
    if "sectors" in attributes and isinstance(attributes["sectors"], list):
        attributes["sectors"] = ",".join(attributes["sectors"])
    return requests.put(
        f"{BASE_URL}/users/update-user",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "uid": user["uid"],
            "attributes": attributes
        }
    ).status_code


def get_ticker_by_code(ticker_code, token) -> Response:
    return requests.get(
        f"{SHARES_URL}/info/{ticker_code}",
        headers={"Authorization": f"Bearer {token}"}
    )


def get_ticker_shareholders(ticker_code, token) -> Response:
    return requests.get(
        f"{SHARES_URL}/holders/{ticker_code}",
        headers={"Authorization": f"Bearer {token}"}
    )

def get_ticker_news(tickers, token) -> Response:
    return requests.get(
        f"{SHARES_URL}/news",
        headers={"Authorization": f"Bearer {token}"},
        json={"tickers": tickers}
    )

def get_tickers_history(tickers, start, end, interval, token) -> Response:
    return requests.post(
        f"{SHARES_URL}/history",
        headers={"Authorization": f"Bearer {token}"},
        json={"tickers": tickers, "start": start, "end": end, "interval": interval}
    )

def get_shareholder_activity(ticker_code, token) -> Response:
    return requests.get(
        f"{SHARES_URL}/activity/{ticker_code}",
        headers={"Authorization": f"Bearer {token}"}
    )

def get_brokers_by_domains(domains, token) -> Response:
    return requests.get(
        f"{BROKERS_URL}/get-by-domains",
        headers={"Authorization": f"Bearer {token}"},
        json={"domains": domains}
    )

def get_all_brokers_except(domains, token) -> Response:
    return requests.get(
        f"{BROKERS_URL}/get-all-except",
        headers={"Authorization": f"Bearer {token}"},
        json={"domains": domains}
    )