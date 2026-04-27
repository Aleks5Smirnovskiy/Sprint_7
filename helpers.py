import random
import string
import time

import allure
import requests

from data import ORDER_BASE_PAYLOAD
from urls import (
    CANCEL_ORDER_PATH,
    CREATE_COURIER_PATH,
    CREATE_ORDER_PATH,
    LOGIN_COURIER_PATH,
    build_url,
    delete_courier_url,
)


def generate_random_string(length: int) -> str:
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for _ in range(length))


def build_courier_payload() -> dict[str, str]:
    return {
        "login": generate_random_string(10),
        "password": generate_random_string(10),
        "firstName": generate_random_string(10),
    }


def build_order_payload(colors=None) -> dict:
    payload = ORDER_BASE_PAYLOAD.copy()
    if colors is not None:
        payload["color"] = colors
    return payload


def request_with_retry(method: str, url: str, retries: int = 4, timeout: int = 20, **kwargs):
    """Retries request on transient server-side failures to reduce flaky tests."""
    transient_statuses = {500, 502, 503, 504}
    response = None

    for attempt in range(retries):
        try:
            response = requests.request(method, url, timeout=timeout, **kwargs)
        except requests.RequestException:
            if attempt < retries - 1:
                time.sleep(1)
                continue
            raise
        if response.status_code not in transient_statuses:
            return response
        if attempt < retries - 1:
            time.sleep(1)

    return response


def create_courier(payload: dict[str, str]):
    return request_with_retry("POST", build_url(CREATE_COURIER_PATH), json=payload)


def login_courier(credentials: dict[str, str]):
    return request_with_retry("POST", build_url(LOGIN_COURIER_PATH), json=credentials)


def delete_courier(credentials: dict[str, str]):
    login_response = login_courier(
        {"login": credentials["login"], "password": credentials["password"]}
    )
    if login_response.status_code == 200 and "id" in login_response.json():
        courier_id = login_response.json()["id"]
        return request_with_retry("DELETE", delete_courier_url(courier_id))
    return login_response


def create_order(payload: dict):
    return request_with_retry("POST", build_url(CREATE_ORDER_PATH), json=payload)


def cancel_order(track: int):
    return request_with_retry("PUT", build_url(CANCEL_ORDER_PATH), params={"track": track})


@allure.step("Register new courier")
def register_new_courier_and_return_login_password(base_url: str) -> list[str]:
    """Returns [login, password, first_name] when registration succeeds, otherwise []."""
    payload = build_courier_payload()

    response = create_courier(payload)

    if response.status_code == 201:
        return [payload["login"], payload["password"], payload["firstName"]]

    return []
