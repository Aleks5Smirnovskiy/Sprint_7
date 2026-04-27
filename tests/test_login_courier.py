import allure
import pytest

from helpers import generate_random_string, request_with_retry


@allure.feature("Courier login")
class TestLoginCourier:
    @allure.title("Courier can login")
    def test_courier_can_login(self, base_url, courier_credentials):
        response = request_with_retry(
            "POST",
            f"{base_url}/api/v1/courier/login",
            json={
                "login": courier_credentials["login"],
                "password": courier_credentials["password"],
            },
        )

        assert response.status_code == 200
        assert "id" in response.json()

    @allure.title("Login requires all required fields")
    @pytest.mark.parametrize("missing_field", ["login"])
    def test_login_missing_required_field_returns_error(self, base_url, missing_field):
        payload = {
            "login": generate_random_string(12),
            "password": generate_random_string(12),
        }
        payload.pop(missing_field)

        response = request_with_retry("POST", f"{base_url}/api/v1/courier/login", json=payload)

        assert response.status_code == 400
        assert "message" in response.json()

    @allure.title("Login fails with wrong credentials")
    def test_login_wrong_credentials_returns_error(self, base_url, courier_credentials):
        response = request_with_retry(
            "POST",
            f"{base_url}/api/v1/courier/login",
            json={
                "login": courier_credentials["login"],
                "password": "wrong-password",
            },
        )

        assert response.status_code == 404
        assert "message" in response.json()

    @allure.title("Login fails for nonexistent user")
    def test_login_nonexistent_user_returns_error(self, base_url):
        response = request_with_retry(
            "POST",
            f"{base_url}/api/v1/courier/login",
            json={
                "login": generate_random_string(12),
                "password": generate_random_string(12),
            },
        )

        assert response.status_code == 404
        assert "message" in response.json()
