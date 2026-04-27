import allure
import pytest

from data import (
    CREATE_COURIER_DUPLICATE_MESSAGE,
    CREATE_COURIER_MISSING_DATA_MESSAGE,
    CREATE_COURIER_SUCCESS_RESPONSE,
)
from helpers import build_courier_payload, create_courier


@allure.feature("Create courier")
class TestCreateCourier:
    @allure.title("Courier can be created")
    def test_create_courier_success(self, courier_cleanup):
        payload = build_courier_payload()

        response = create_courier(payload)
        courier_cleanup.append(payload)

        assert response.status_code == 201
        assert response.json() == CREATE_COURIER_SUCCESS_RESPONSE

    @allure.title("Cannot create duplicate courier")
    def test_create_duplicate_courier_returns_error(self, courier_cleanup):
        payload = build_courier_payload()

        first_response = create_courier(payload)
        if first_response.status_code != 201:
            pytest.fail("Could not create courier for duplicate test setup")

        courier_cleanup.append(payload)
        second_response = create_courier(payload)

        assert second_response.status_code == 409
        assert second_response.json()["message"] == CREATE_COURIER_DUPLICATE_MESSAGE

    @allure.title("Cannot create courier without required login")
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_create_courier_missing_required_field_returns_error(self, missing_field):
        payload = build_courier_payload()
        payload.pop(missing_field)

        response = create_courier(payload)

        assert response.status_code == 400
        assert response.json()["message"] == CREATE_COURIER_MISSING_DATA_MESSAGE
