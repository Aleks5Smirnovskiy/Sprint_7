import allure
import pytest

from helpers import register_new_courier_and_return_login_password, request_with_retry


@pytest.fixture(scope="session")
def base_url() -> str:
    return "https://qa-scooter.education-services.ru"


@pytest.fixture
def courier_credentials(base_url: str) -> dict[str, str]:
    login, password, first_name = register_new_courier_and_return_login_password(base_url)
    if not login:
        pytest.fail("Could not create courier for test setup")

    credentials = {
        "login": login,
        "password": password,
        "firstName": first_name,
    }

    yield credentials

    with allure.step("Delete created courier"):
        login_response = request_with_retry(
            "POST",
            f"{base_url}/api/v1/courier/login",
            json={"login": login, "password": password},
        )
        if login_response.status_code == 200 and "id" in login_response.json():
            courier_id = login_response.json()["id"]
            request_with_retry("DELETE", f"{base_url}/api/v1/courier/{courier_id}")
