# region Ошибки полей
from time import time

import pytest

FIELD_REQUIRED_ERROR = "Заполните это поле."
FIELD_EMAIL_ERROR = 'Адрес электронной почты должен содержать символ "@". В адресе "{email}" отсутствует символ "@".'
FIELD_EMAIL_EXISTING_ERROR = "Email Address already exist!"
# endregion

# region Валидные поля
VALID_NAME = f"valid_name-{time()}"
VALID_EMAIL = f"valid-email-{time()}@mail.ru"
# endregion

# region Невалидные поля
EMPTY_FIELD = ""
INVALID_EMAIL = "invalid-email"
EXISTING_EMAIL = "admin@mail.ru"
# endregion

invalid_names = [
    pytest.param(
        {"name": EMPTY_FIELD, "email": VALID_EMAIL}, FIELD_REQUIRED_ERROR,
        id=f"name: {EMPTY_FIELD} | email: {VALID_EMAIL}"
    ),
]

invalid_emails = [
    pytest.param(
        {"name": VALID_NAME, "email": EMPTY_FIELD}, FIELD_REQUIRED_ERROR,
        id=f"name: {VALID_NAME} | email: {EMPTY_FIELD}"
    ),
    pytest.param(
        {"name": VALID_NAME, "email": INVALID_EMAIL}, FIELD_EMAIL_ERROR.format(email=INVALID_EMAIL),
        id=f"name: {VALID_NAME} | email: {INVALID_EMAIL}"
    ),
    pytest.param(
        {"name": VALID_NAME, "email": EXISTING_EMAIL}, FIELD_EMAIL_EXISTING_ERROR,
        id=f"name: {VALID_NAME} | email: {EXISTING_EMAIL}"
    ),
]

invalid_account_information_data = [
    pytest.param(
        {
            "name": VALID_NAME,
            "email": VALID_EMAIL,
            "title": "Mr",
            "edited_name": VALID_NAME + "_EDITED",
            "password": "",
            "receive_newsletters": True,
            "receive_offers": True,
            "date_or_birth": "20-3-2000",
            "first_name": "first",
            "last_name": "last",
            "company": "company1",
            "address1": "address1",
            "address2": None,
            "country": "Australia",
            "state": "state",
            "city": "City1",
            "zipcode": 35000,
            "mobile_number": "79182222222"
        },
        "password",
        FIELD_REQUIRED_ERROR,
        id="Ввод пустого пароля"
    ),
]
