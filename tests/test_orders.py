import allure
import pytest

from helpers import request_with_retry


@allure.feature("Orders")
class TestOrders:
    @allure.title("Create order with different color combinations")
    @pytest.mark.parametrize(
        "colors",
        [
            ["BLACK"],
            ["GREY"],
            ["BLACK", "GREY"],
            None,
        ],
    )
    def test_create_order_returns_track(self, base_url, colors):
        payload = {
            "firstName": "Naruto",
            "lastName": "Uchiha",
            "address": "Konoha, 142 apt.",
            "metroStation": 4,
            "phone": "+7 800 355 35 35",
            "rentTime": 5,
            "deliveryDate": "2026-04-30",
            "comment": "Saske, come back to Konoha",
        }
        if colors is not None:
            payload["color"] = colors

        response = request_with_retry("POST", f"{base_url}/api/v1/orders", json=payload)

        assert response.status_code == 201
        assert "track" in response.json()

    @allure.title("Orders list is returned in response body")
    def test_get_orders_returns_orders_list(self, base_url):
        response = request_with_retry("GET", f"{base_url}/api/v1/orders")

        assert response.status_code == 200
        body = response.json()
        assert "orders" in body
        assert isinstance(body["orders"], list)
