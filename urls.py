BASE_URL = "https://qa-scooter.education-services.ru"

CREATE_COURIER_PATH = "/api/v1/courier"
LOGIN_COURIER_PATH = "/api/v1/courier/login"
DELETE_COURIER_PATH = "/api/v1/courier/{courier_id}"
CREATE_ORDER_PATH = "/api/v1/orders"
CANCEL_ORDER_PATH = "/api/v1/orders/cancel"
LIST_ORDERS_PATH = "/api/v1/orders"


def build_url(path: str) -> str:
    return f"{BASE_URL}{path}"


def delete_courier_url(courier_id: int) -> str:
    return build_url(DELETE_COURIER_PATH.format(courier_id=courier_id))