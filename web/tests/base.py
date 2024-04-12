import allure


class BaseTest:

    @staticmethod
    def handle_assertion_error(driver, error_message):
        with allure.step("Произошла ошибка"):
            allure.attach(
                driver.get_screenshot_as_png(),
                name="screenshot.png",
                attachment_type=allure.attachment_type.PNG,
            )
            raise AssertionError(error_message)
