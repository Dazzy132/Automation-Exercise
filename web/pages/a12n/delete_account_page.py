import allure

from web.pages.base import WebPage


class DeleteAccountPageLocator:
    delete_button = ("xpath", "//a[@href='/delete_account']")
    account_deleted_msg = ("xpath", "//b[text()='Account Deleted!']")
    continue_button = ("xpath", "//a[@href='/']")


class DeleteAccountPage(WebPage):

    def click_delete_button(self):

        if self.get_current_url() != self._base_url:
            self.go_to_site()

        with allure.step('Нажимаем на кнопку удаления аккаунта'):
            self.find_element(DeleteAccountPageLocator.delete_button).click()

    def check_success_after_deletion_account_msg(self):
        with allure.step("Проверяем что сообщение об успешном удалении аккаунта вывелось"):
            return self.find_element(DeleteAccountPageLocator.account_deleted_msg)

    def click_after_delete_account_button(self):
        with allure.step("Нажимаем на кнопку продолжить"):
            self.find_element(DeleteAccountPageLocator.continue_button).click()
