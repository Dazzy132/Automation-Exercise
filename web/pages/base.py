import time

import allure
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from termcolor import colored


class WebPage:
    _web_driver = None

    def __init__(self, driver):
        self._web_driver = driver
        self._base_url = "https://automationexercise.com/"

    def find_element(self, locator: tuple[str, str], timeout=10):
        return WebDriverWait(self._web_driver, timeout).until(EC.presence_of_element_located(locator))

    # def find_elements(self, locator: tuple[str, str], timeout=10):
    #     return WebDriverWait(self._web_driver, timeout).until(EC.presence_of_element_located(locator))

    def go_to_site(self):
        """Перейти на главную страницу в браузере и дождаться полной загрузки страницы"""
        with allure.step(f"Переходим на главную страницу {self._base_url}"):
            self._web_driver.get(self._base_url)
        # self.wait_page_loaded()

    def go_back(self):
        """Вернуться на предыдущую страницу в браузере и дождаться полной загрузки страницы"""
        self._web_driver.back()
        # self.wait_page_loaded()

    def refresh(self):
        "Обновить страницу и дождаться полной загрузки страницы"
        self._web_driver.refresh()
        # self.wait_page_loaded()

    def save_screenshot(self, file_name='screenshot.png'):
        """Сделать скриншот в браузере и сохранить его"""
        self._web_driver.save_screenshot(file_name)

    def scroll_down(self, offset=0):
        """Прокрутить страницу вниз"""

        if offset:
            self._web_driver.execute_script('window.scrollTo(0, {0});'.format(offset))
        else:
            self._web_driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')

    def scroll_up(self, offset=0):
        """Прокрутить страницу вверх"""

        if offset:
            self._web_driver.execute_script('window.scrollTo(0, -{0});'.format(offset))
        else:
            self._web_driver.execute_script('window.scrollTo(0, -document.body.scrollHeight);')

    def switch_to_iframe(self, iframe):
        """Переключиться на iframe"""

        self._web_driver.switch_to.frame(iframe)

    def switch_out_iframe(self):
        """Выйти из iframe"""
        self._web_driver.switch_to.default_content()

    def get_current_url(self):
        """Получить текущий адрес страницы"""

        return self._web_driver.current_url

    def get_page_source(self):
        """Получить код страницы"""

        source = ''
        try:
            source = self._web_driver.page_source
        except Exception as error:
            print(colored(error, 'red'))

        return source

    def check_js_errors(self, ignore_list=None):
        """Эта функция проверяет ошибки JS на странице. """

        ignore_list = ignore_list or []

        logs = self._web_driver.get_log('browser')
        for log_message in logs:
            if log_message['level'] != 'WARNING':
                ignore = False
                for issue in ignore_list:
                    if issue in log_message['message']:
                        ignore = True
                        break

                assert ignore, 'JS error "{0}" on the page!'.format(log_message)

    def wait_page_loaded(self,
                         timeout=60,
                         check_js_complete=True,
                         check_page_changes=False,
                         wait_for_element=None,
                         wait_for_xpath_to_disappear='',
                         sleep_time=2):
        """ Эта функция ожидает полной загрузки страницы.
            Здесь используется несколько различных способов для определения, загружена ли страница или нет:

            1. Проверка статуса JS
            2. Проверка изменений в исходном коде страницы
            3. Проверка наличия ожидаемых элементов на странице
        """

        page_loaded = False
        double_check = False
        k = 0

        if sleep_time:
            time.sleep(sleep_time)

        # Получить исходный код страницы для отслеживания изменений в HTML
        source = ''
        try:
            source = self._web_driver.page_source
        except Exception as error:
            print(colored(error, 'red'))

        # Дожидаемся загрузки страницы (и прокрутить её вниз, чтобы убедиться, что все объекты будут загружены)
        while not page_loaded:
            time.sleep(0.5)
            k += 1

            # Проверка, что весь JS код отработал.
            if check_js_complete:
                # Прокрутка страницы вниз и ожидание загрузки страницы:
                try:
                    self._web_driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                    page_loaded = self._web_driver.execute_script("return document.readyState == 'complete';")
                except Exception as error:
                    print(colored(error, 'red'))

            # Проверка на изменение в исходном коде страницы после её полной загрузки
            if page_loaded and check_page_changes:
                new_source = ''
                try:
                    new_source = self._web_driver.page_source
                except Exception as error:
                    print(colored(error, 'red'))

                page_loaded = new_source == source
                source = new_source

            # Проверка на то, что элемент исчезнет со страницы (Loader или т.п.)
            if page_loaded and wait_for_xpath_to_disappear:
                bad_element = None

                try:
                    bad_element = WebDriverWait(self._web_driver, 0.1).until(
                        EC.presence_of_element_located(("xpath", wait_for_xpath_to_disappear))
                    )
                except Exception as error:
                    print(colored(error, 'red'))

                # Если элемент найден на странице - то она еще не загрузилась. Если же не найден - загрузилась.
                page_loaded = not bad_element

            # Проверка на то, что страница полностью загрузится и элемент на странице отобразится
            if page_loaded and wait_for_element:
                try:
                    page_loaded = WebDriverWait(self._web_driver, 0.1).until(
                        EC.element_to_be_clickable(wait_for_element._locator)
                    )
                except Exception as error:
                    print(colored(error, 'red'))

            assert k < timeout, f'The page loaded more than {timeout} seconds!'

            # Дополнительная проверка на то, что страница загрузилась
            if page_loaded and not double_check:
                page_loaded = False
                double_check = True

        # Пролистать страницу вверх
        self._web_driver.execute_script('window.scrollTo(document.body.scrollHeight, 0);')
