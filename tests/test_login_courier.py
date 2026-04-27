import allure
import pytest

from data import (
    LOGIN_COURIER_ACCOUNT_NOT_FOUND_MESSAGE,
    LOGIN_COURIER_MISSING_DATA_MESSAGE,
)
from helpers import build_courier_payload, login_courier


@allure.feature("Courier login")
class TestLoginCourier:
    @allure.title("Courier can login")
    def test_courier_can_login(self, courier_credentials):
        response = login_courier(
            {
                "login": courier_credentials["login"],
                "password": courier_credentials["password"],
            }
        )

        assert response.status_code == 200
        assert "id" in response.json()

    @allure.title("Login requires all required fields")
    @pytest.mark.parametrize("missing_field", ["login"])
    def test_login_missing_required_field_returns_error(self, missing_field):
        payload = build_courier_payload()
        payload.pop(missing_field)

        response = login_courier(payload)

        assert response.status_code == 400
        assert response.json()["message"] == LOGIN_COURIER_MISSING_DATA_MESSAGE

    @allure.title("Login fails with wrong credentials")
    def test_login_wrong_credentials_returns_error(self, courier_credentials):
        response = login_courier(
            {
                "login": courier_credentials["login"],
                "password": "wrong-password",
            }
        )

        assert response.status_code == 404
        assert response.json()["message"] == LOGIN_COURIER_ACCOUNT_NOT_FOUND_MESSAGE

    @allure.title("Login fails for nonexistent user")
    def test_login_nonexistent_user_returns_error(self):
        payload = build_courier_payload()
        response = login_courier(
            {
                "login": payload["login"],
                "password": payload["password"],
            }
        )

        assert response.status_code == 404
        assert response.json()["message"] == LOGIN_COURIER_ACCOUNT_NOT_FOUND_MESSAGE
