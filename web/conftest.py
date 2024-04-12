import json
import allure
import os

import pytest

from selenium import webdriver
from selenium.webdriver.chrome.service import Service

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
