import allure
from selenium.webdriver.support.select import Select

from web.pages.base import WebPage
from .utils import AccountInfo


class SignUpLocator:
    """Локаторы полей на странице с Аутентификацией"""
    NAME_INPUT = ("xpath", "//form[@action='/signup']/input[@name='name']")
    EMAIL_INPUT = ("xpath", "//form[@action='/signup']/input[@name='email']")
    SUBMIT_BUTTON = ("xpath", "//form[@action='/signup']/button[@type='submit']")
    H2_TEXT = ("xpath", "//h2[text()='New User Signup!']")


class AccountInfLocator:
    """Локаторы полей на странице ввода дополнительной информации"""
    ACCOUNT_INFORMATION_TEXT = ("xpath", "//b[text()='Enter Account Information']")
    GENDER_MR_RADIO = ("xpath", "//input[@id='id_gender1']")
    GENDER_MRS_RADIO = ("xpath", "//input[@id='id_gender2']")
    NAME_INPUT = ("xpath", "//input[@id='name']")
    PASSWORD_INPUT = ("xpath", "//input[@id='password']")
    BIRTH_DAY_SELECT = ("xpath", "//select[@id='days']")
    BIRTH_MONTH_SELECT = ("xpath", "//select[@id='months']")
    BIRTH_YEAR_SELECT = ("xpath", "//select[@id='years']")
    SIGNUP_FOR_NEWSLETTER_INPUT = ("xpath", "//input[@id='newsletter']")
    RECEIVE_SPECIAL_OFFERS_INPUT = ("xpath", "//input[@id='optin']")
    FIRST_NAME_INPUT = ("xpath", "//input[@id='first_name']")
    LAST_NAME_INPUT = ("xpath", "//input[@id='last_name']")
    COMPANY_INPUT = ("xpath", "//input[@id='company']")
    ADDRESS1_INPUT = ("xpath", "//input[@id='address1']")
    ADDRESS2_INPUT = ("xpath", "//input[@id='address2']")
    COUNTRY_SELECT = ("xpath", "//select[@id='country']")
    STATE_INPUT = ("xpath", "//input[@id='state']")
    CITY_INPUT = ("xpath", "//input[@id='city']")
    ZIPCODE_INPUT = ("xpath", "//input[@id='zipcode']")
    MOBILE_NUMBER_INPUT = ("xpath", "//input[@id='mobile_number']")
    CREATE_ACCOUNT_BUTTON = ("xpath", "//button[@type='submit' and @data-qa='create-account']")


class AfterRegistrationPageLocator:
    """Локаторы полей на странице после регистрации"""
    success_creation_msg = ("xpath", "//b[text()='Account Created!']")
    continue_button = ("xpath", "//a[@href='/']")


class SignUpPage(WebPage):

    def check_signup_page_is_loaded(self):
        """Посмотреть что страница с регистрацией загрузилась"""
        with allure.step("Страница с регистрацией загрузилась"):
            return self.find_element(SignUpLocator.H2_TEXT).is_displayed()

    def check_account_information_page_is_loaded(self):
        """Посмотреть что страница с вводом дополнительной информации загрузилась"""
        with allure.step("Страница с вводом дополнительной информации загрузилась"):
            return self.find_element(AccountInfLocator.ACCOUNT_INFORMATION_TEXT).is_displayed()

    def check_success_registration_msg(self):
        """Посмотреть что выведено сообщение об успешной регистрации"""
        with allure.step("Сообщение об успешной регистрации выведено"):
            return self.find_element(AfterRegistrationPageLocator.success_creation_msg)

    def click_create_account_button(self):
        """Нажать на кнопку создать аккаунт в дополнительной информации"""
        with allure.step("Нажимаем на кнопку создать аккаунт"):
            self.find_element(AccountInfLocator.CREATE_ACCOUNT_BUTTON).click()

    def click_after_registration_continue_button(self):
        """Нажать на кнопку после регистрации и ввода дополнительной информации. Чтобы завершить регистрацию"""
        with allure.step("Нажимаем на кнопку продолжить"):
            self.find_element(AfterRegistrationPageLocator.continue_button).click()

    def enter_login_and_email_data(self, name, email):
        """Ввести данные в поля вода (для регистрации)"""
        with allure.step("Вводим имя"):
            self.find_element(SignUpLocator.NAME_INPUT).send_keys(name)
        with allure.step("Вводим пароль"):
            self.find_element(SignUpLocator.EMAIL_INPUT).send_keys(email)
        with allure.step("Нажимаем на кнопку зарегистрироваться"):
            self.find_element(SignUpLocator.SUBMIT_BUTTON).click()

    def enter_account_information_data(self, data: AccountInfo):
        """Ввести в поля дополнительную информацию об аккаунте"""

        with allure.step(f"Вводим гендер {data['title']}"):
            self.find_element(
                AccountInfLocator.GENDER_MR_RADIO if data["title"].lower() == "mr"
                else AccountInfLocator.GENDER_MRS_RADIO
            ).click()

        if data["edited_name"]:
            with allure.step(f"Изменяем имя с {data['name']} на {data['edited_name']}"):
                name_input = self.find_element(AccountInfLocator.NAME_INPUT)
                name_input.clear()
                name_input.send_keys(data["edited_name"])

        with allure.step(f"Вводим пароль {data['password']}"):
            self.find_element(AccountInfLocator.PASSWORD_INPUT).send_keys(data["password"])

        d, m, y = data["date_or_birth"].split("-")
        with allure.step(f"Вводим дату рождения {d}-{m}-{y}"):
            Select(self.find_element(AccountInfLocator.BIRTH_DAY_SELECT)).select_by_value(d)
            Select(self.find_element(AccountInfLocator.BIRTH_MONTH_SELECT)).select_by_value(m)
            Select(self.find_element(AccountInfLocator.BIRTH_YEAR_SELECT)).select_by_value(y)

        if data["receive_newsletters"]:
            with allure.step("Подписываемся на рассылку новостей"):
                self.find_element(AccountInfLocator.SIGNUP_FOR_NEWSLETTER_INPUT).click()

        if data["receive_offers"]:
            with allure.step("Подписываемся на рассылку предложений"):
                self.find_element(AccountInfLocator.RECEIVE_SPECIAL_OFFERS_INPUT).click()

        with allure.step(f"Вводим имя {data['first_name']}"):
            self.find_element(AccountInfLocator.FIRST_NAME_INPUT).send_keys(data["first_name"])

        with allure.step(f"Вводим фамилию {data['last_name']}"):
            self.find_element(AccountInfLocator.LAST_NAME_INPUT).send_keys(data["last_name"])

        if data["company"]:
            with allure.step(f"Вводим название компании {data['company']}"):
                self.find_element(AccountInfLocator.COMPANY_INPUT).send_keys(data["company"])

        with allure.step(f"Вводим основной адрес {data['address1']}"):
            self.find_element(AccountInfLocator.ADDRESS1_INPUT).send_keys(data["address1"])

        if data["address2"]:
            with allure.step(f"Вводим дополнительный адрес {data['address2']}"):
                self.find_element(AccountInfLocator.ADDRESS2_INPUT).send_keys(data["address2"])

        with allure.step(f"Вводим страну {data['country']}"):
            Select(self.find_element(AccountInfLocator.COUNTRY_SELECT)).select_by_value(data["country"])

        with allure.step(f"Вводим штат {data['state']}"):
            self.find_element(AccountInfLocator.STATE_INPUT).send_keys(data["state"])

        with allure.step(f"Вводим город {data['city']}"):
            self.find_element(AccountInfLocator.CITY_INPUT).send_keys(data["city"])

        with allure.step(f"Вводим zipcode {data['zipcode']}"):
            self.find_element(AccountInfLocator.ZIPCODE_INPUT).send_keys(data["zipcode"])

        with allure.step(f"Вводим номер мобильного телефона {data['mobile_number']}"):
            self.find_element(AccountInfLocator.MOBILE_NUMBER_INPUT).send_keys(data["mobile_number"])
