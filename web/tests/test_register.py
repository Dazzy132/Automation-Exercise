import time

import allure
import pytest
from selenium.webdriver.chrome.webdriver import WebDriver

from web.conftest import get_registration_params
from web.pages import MainPage, SignUpPage, DeleteAccountPage
from web.pages.a12n.signup_page import SignUpLocator, AccountInfLocator
from web.tests import BaseTest
from .invalid_data import (invalid_names, invalid_emails, EXISTING_EMAIL, FIELD_EMAIL_EXISTING_ERROR,
                           invalid_account_information_data
                           )

registration_params = get_registration_params()


@allure.title("Test Case 1: Register User")
@allure.description("Этот тест пытается зарегистрировать пользователя на сайте с валидными данными")
@allure.tag("Authentication")
@allure.severity("blocker")
class TestRegistration(BaseTest):

    @staticmethod
    def open_main_page(driver) -> MainPage:
        main_page = MainPage(driver)
        main_page.go_to_site()
        assert main_page.check_page_is_loaded(), "Страница не загрузилась"

        return main_page

    @staticmethod
    def open_signup_page(driver: WebDriver, main_page: MainPage) -> SignUpPage:
        main_page.click_signup_button()
        signup_page = SignUpPage(driver)
        assert signup_page.check_signup_page_is_loaded(), "Страница регистрации не загрузилась"

        return signup_page

    @staticmethod
    def enter_registration_data_on_signup_page(signup_page: SignUpPage, reg_params) -> None:
        signup_page.enter_login_and_email_data(name=reg_params['name'], email=reg_params['email'])
        assert signup_page.check_account_information_page_is_loaded(), ("Страница с дополнительной информацией"
                                                                        " не загрузилась")

    @staticmethod
    def enter_account_information_data_on_signup_page(signup_page: SignUpPage, reg_params) -> None:
        signup_page.enter_account_information_data(reg_params)
        signup_page.click_create_account_button()
        assert signup_page.check_success_registration_msg().is_displayed(), "Сообщение об успешной регистрации нет"
        assert signup_page.check_success_registration_msg().text == "ACCOUNT CREATED!"
        signup_page.click_after_registration_continue_button()

    @staticmethod
    def delete_account_after_registration(driver: WebDriver) -> None:
        delete_page = DeleteAccountPage(driver)
        delete_page.click_delete_button()
        assert delete_page.check_success_after_deletion_account_msg().is_displayed()
        assert delete_page.check_success_after_deletion_account_msg().text == "ACCOUNT DELETED!"

        delete_page.click_after_delete_account_button()

    @pytest.mark.skip("Работает")
    @pytest.mark.parametrize(
        "reg_params", registration_params,
        ids=[f"Name: {param['name']} | Email: {param['email']}" for param in registration_params]
    )
    def test_valid_register_and_delete_user(self, driver, reg_params):
        main_page = self.open_main_page(driver)
        signup_page = self.open_signup_page(driver, main_page)
        self.enter_registration_data_on_signup_page(signup_page, reg_params)
        self.enter_account_information_data_on_signup_page(signup_page, reg_params)
        self.delete_account_after_registration(driver)

    @pytest.mark.skip("Работает")
    @pytest.mark.parametrize(
        "reg_params, excepted_msg", invalid_names
    )
    def test_invalid_name(self, driver, reg_params: dict, excepted_msg: str):
        main_page = self.open_main_page(driver)
        signup_page = self.open_signup_page(driver, main_page)

        name_input = signup_page.find_element(SignUpLocator.NAME_INPUT)
        signup_page.enter_login_and_email_data(name=reg_params['name'], email=reg_params['email'])

        assert name_input.get_attribute("validationMessage") == excepted_msg

    @pytest.mark.skip("Работает")
    @pytest.mark.parametrize(
        "reg_params, excepted_msg", invalid_emails
    )
    def test_invalid_email(self, driver, reg_params: dict, excepted_msg: str):
        main_page = self.open_main_page(driver)
        signup_page = self.open_signup_page(driver, main_page)

        email_input = signup_page.find_element(SignUpLocator.EMAIL_INPUT)
        signup_page.enter_login_and_email_data(name=reg_params['name'], email=reg_params['email'])

        if reg_params["email"] != EXISTING_EMAIL:
            assert email_input.get_attribute("validationMessage") == excepted_msg
        else:
            assert signup_page.find_element(("xpath", f"//p[text()='{FIELD_EMAIL_EXISTING_ERROR}']")).is_displayed()

    @pytest.mark.parametrize(
        "reg_params, invalid_input_name, excepted_msg", invalid_account_information_data
    )
    def test_invalid_account_information_data(self, driver, reg_params: dict, invalid_input_name, excepted_msg):
        main_page = self.open_main_page(driver)
        signup_page = self.open_signup_page(driver, main_page)
        signup_page.enter_login_and_email_data(name=reg_params["name"], email=reg_params["email"])

        invalid_input_names = {
            "name": signup_page.find_element(AccountInfLocator.NAME_INPUT),
            "password": signup_page.find_element(AccountInfLocator.PASSWORD_INPUT),
        }

        signup_page.enter_account_information_data(reg_params)

        if reg_params["edited_name"]:
            assert invalid_input_names["name"].get_attribute("value") == reg_params["edited_name"], "Имя не изменилось"

        signup_page.click_create_account_button()

        assert invalid_input_names[invalid_input_name].get_attribute("validationMessage") == excepted_msg

