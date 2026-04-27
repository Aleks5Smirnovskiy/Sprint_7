import allure
import pytest

from helpers import generate_random_string, request_with_retry


@allure.feature("Create courier")
class TestCreateCourier:
    @allure.title("Courier can be created")
    def test_create_courier_success(self, base_url):
        payload = {
            "login": generate_random_string(10),
            "password": generate_random_string(10),
            "firstName": generate_random_string(10),
        }

        response = request_with_retry("POST", f"{base_url}/api/v1/courier", json=payload)

        assert response.status_code == 201
        assert response.json() == {"ok": True}

    @allure.title("Cannot create duplicate courier")
    def test_create_duplicate_courier_returns_error(self, base_url):
        payload = {
            "login": generate_random_string(10),
            "password": generate_random_string(10),
            "firstName": generate_random_string(10),
        }

        first_response = request_with_retry("POST", f"{base_url}/api/v1/courier", json=payload)
        second_response = request_with_retry("POST", f"{base_url}/api/v1/courier", json=payload)

        assert first_response.status_code == 201
        assert second_response.status_code == 409
        assert "message" in second_response.json()

    @allure.title("Cannot create courier without required login")
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_create_courier_missing_required_field_returns_error(self, base_url, missing_field):
        payload = {
            "login": generate_random_string(10),
            "password": generate_random_string(10),
            "firstName": generate_random_string(10),
        }
        payload.pop(missing_field)

        response = request_with_retry("POST", f"{base_url}/api/v1/courier", json=payload)

        assert response.status_code == 400
        assert "message" in response.json()
