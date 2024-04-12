import allure
import pytest
from selenium.webdriver.chrome.webdriver import WebDriver

from web.conftest import get_registration_params
from web.pages import MainPage, SignUpPage, DeleteAccountPage
from web.pages.a12n.signup_page import SignUpLocator
from web.tests import BaseTest

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

    @pytest.mark.smoke
    @pytest.mark.parametrize(
        "reg_params, problem_field, excepted_msg",
        [
            pytest.param(
                {"name": "", "email": ""}, "name", "Заполните это поле.",
                id="name: '' | email: ''"
            ),
            pytest.param(
                {"name": "", "email": "test-valid-email-email@mail.ru"}, "name", "Заполните это поле.",
                id="name: '' | email: test-valid-email-email@mail.ru"
            ),
            pytest.param(
                {"name": "TestNameValid", "email": ""}, "email", "Заполните это поле.",
                id="name: TestNameValid | email: ''"
            ),
            pytest.param(
                {"name": "TestNameValid", "email": "InvalidEmail"},
                "email",
                "Адрес электронной почты должен содержать символ \"@\". "
                "В адресе \"InvalidEmail\" отсутствует символ \"@\".",
                id="name: TestNameValid | email: InvalidEmail"
            )
        ]
    )
    def test_invalid_registration_data(self, driver, reg_params, problem_field, excepted_msg):
        main_page = self.open_main_page(driver)
        signup_page = self.open_signup_page(driver, main_page)

        input_elements = {
            "name": signup_page.find_element(SignUpLocator.NAME_INPUT),
            "email": signup_page.find_element(SignUpLocator.EMAIL_INPUT)
        }

        for field_name, element in input_elements.items():
            element.send_keys(reg_params[field_name])

        assert input_elements[problem_field].get_attribute("validationMessage") == excepted_msg
