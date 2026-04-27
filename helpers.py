import random
import string
import time

import allure
import requests


def generate_random_string(length: int) -> str:
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for _ in range(length))


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


@allure.step("Register new courier")
def register_new_courier_and_return_login_password(base_url: str) -> list[str]:
    """Returns [login, password, first_name] when registration succeeds, otherwise []."""
    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)

    payload = {
        "login": login,
        "password": password,
        "firstName": first_name,
    }

    response = request_with_retry("POST", f"{base_url}/api/v1/courier", json=payload)

    if response.status_code == 201:
        return [login, password, first_name]

    return []
