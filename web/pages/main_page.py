import allure

from web.pages.base import WebPage


class MainPageLocator:
    SIGNUP_BUTTON = ("xpath", "//a[@href='/login']")
    MAIN_BANNER = ("xpath", "//div[@class='carousel-inner']")


class MainPage(WebPage):

    def click_signup_button(self):
        with allure.step(f"Нажимаем на кнопку регистрации пользователя"):
            self.find_element(MainPageLocator.SIGNUP_BUTTON).click()

    def check_page_is_loaded(self):
        with allure.step(f"Проверка на то, что главная страница загрузилась"):
            return self.find_element(MainPageLocator.MAIN_BANNER).is_displayed()
