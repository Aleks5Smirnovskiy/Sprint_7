import allure
import pytest

from helpers import (
    build_courier_payload,
    cancel_order,
    create_courier,
    delete_courier,
)


@pytest.fixture
def courier_cleanup():
    created_couriers = []

    yield created_couriers

    for credentials in created_couriers:
        with allure.step("Delete created courier"):
            delete_courier(credentials)


@pytest.fixture
def courier_credentials(courier_cleanup) -> dict[str, str]:
    credentials = build_courier_payload()
    response = create_courier(credentials)
    if response.status_code != 201:
        pytest.fail("Could not create courier for test setup")

    courier_cleanup.append(credentials)

    return credentials


@pytest.fixture
def order_cleanup():
    created_tracks = []

    yield created_tracks

    for track in created_tracks:
        with allure.step("Cancel created order"):
            cancel_order(track)
