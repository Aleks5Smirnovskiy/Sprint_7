CREATE_COURIER_SUCCESS_RESPONSE = {"ok": True}
CREATE_COURIER_DUPLICATE_MESSAGE = "Этот логин уже используется. Попробуйте другой."
CREATE_COURIER_MISSING_DATA_MESSAGE = "Недостаточно данных для создания учетной записи"

LOGIN_COURIER_MISSING_DATA_MESSAGE = "Недостаточно данных для входа"
LOGIN_COURIER_ACCOUNT_NOT_FOUND_MESSAGE = "Учетная запись не найдена"

ORDER_BASE_PAYLOAD = {
    "firstName": "Naruto",
    "lastName": "Uchiha",
    "address": "Konoha, 142 apt.",
    "metroStation": 4,
    "phone": "+7 800 355 35 35",
    "rentTime": 5,
    "deliveryDate": "2026-04-30",
    "comment": "Saske, come back to Konoha",
}

ORDER_COLORS = [
    ["BLACK"],
    ["GREY"],
    ["BLACK", "GREY"],
    None,
]