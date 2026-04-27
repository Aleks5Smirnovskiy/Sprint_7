import allure
import pytest

from data import ORDER_COLORS
from helpers import build_order_payload, create_order, request_with_retry
from urls import LIST_ORDERS_PATH, build_url


@allure.feature("Orders")
class TestOrders:
    @allure.title("Create order with different color combinations")
    @pytest.mark.parametrize("colors", ORDER_COLORS)
    def test_create_order_returns_track(self, order_cleanup, colors):
        payload = build_order_payload(colors)

        response = create_order(payload)
        track = response.json()["track"]
        order_cleanup.append(track)

        assert response.status_code == 201
        assert "track" in response.json()

    @allure.title("Orders list is returned in response body")
    def test_get_orders_returns_orders_list(self):
        response = request_with_retry("GET", build_url(LIST_ORDERS_PATH))

        assert response.status_code == 200
        body = response.json()
        assert "orders" in body
        assert isinstance(body["orders"], list)
