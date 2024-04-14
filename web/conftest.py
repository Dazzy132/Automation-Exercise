import json
import allure
import os

import pytest

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.remote.webelement import WebElement

from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture(scope="session")
def driver():
    """Инициализация и настройка браузера"""

    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")
    # options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-dev-shm-usage")

    service = Service(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    with allure.step("Запускаем браузер"):
        yield driver

        driver.quit()


def get_registration_params():
    """Получить данные пользователи из json файла"""
    filepath = os.path.join(os.path.dirname(__file__), "test-data/registration_params.json")

    with open(filepath, "r", encoding="UTF-8") as reg_params:
        return json.load(reg_params)


def fill_input_fields(elements_to_fill: dict[str, WebElement], params_to_fill: dict[str, str]):
    """
    :param elements_to_fill: [email_field: WebElement]
    :param params_to_fill: [email: email@mail.ru]
    """
    for field_name, element in elements_to_fill.items():
        element.send_keys(params_to_fill[field_name])