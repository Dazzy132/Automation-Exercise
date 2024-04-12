import allure
import pytest

from web.tests import BaseTest
from web.pages import MainPage, SignUpPage, DeleteAccountPage
from web.conftest import get_registration_params

registration_params = get_registration_params()


@allure.title("Test Case 1: Register User")
@allure.description("Этот тест пытается зарегистрировать пользователя на сайте с валидными данными")
@allure.tag("Authentication")
@allure.severity("blocker")
class TestRegistration(BaseTest):

    @pytest.mark.parametrize(
        "reg_params", registration_params,
        ids=[f"Name: {param['name']} | Email: {param['email']}" for param in registration_params]
    )
    def test_register_and_delete_user(self, driver, reg_params):

        # Open Main Page
        main_page = MainPage(driver)
        main_page.go_to_site()
        assert main_page.check_page_is_loaded(), "Страница не загрузилась"

        # Switch to Signup Page
        main_page.click_signup_button()
        signup_page = SignUpPage(driver)
        assert signup_page.check_signup_page_is_loaded(), "Страница регистрации не загрузилась"

        # Enter the registration data
        signup_page.enter_login_and_email_data(name=reg_params['name'], email=reg_params['email'])
        assert signup_page.check_account_information_page_is_loaded(), ("Страница с дополнительной информацией"
                                                                        " не загрузилась")

        # Enter account information data
        signup_page.enter_account_information_data(reg_params)

        # Click Create Account Button
        signup_page.click_create_account_button()

        # After Registration
        assert signup_page.check_success_registration_msg().is_displayed(), "Сообщение об успешной регистрации нет"
        assert signup_page.check_success_registration_msg().text == "ACCOUNT CREATED!"

        signup_page.click_after_registration_continue_button()

        delete_page = DeleteAccountPage(driver)
        delete_page.click_delete_button()
        assert delete_page.check_success_after_deletion_account_msg().is_displayed()
        assert delete_page.check_success_after_deletion_account_msg().text == "ACCOUNT DELETED!"

        delete_page.click_after_delete_account_button()
