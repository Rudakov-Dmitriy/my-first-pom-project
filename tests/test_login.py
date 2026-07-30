import pytest
from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from config import settings
from config import settings

# "standard_user" → settings.LOGIN
# "secret_sauce" → settings.PASSWORD


class TestLogin:
    """Тесты страницы логина SauceDemo."""

    def test_successful_login(self, page):
        """Позитивный тест: логин со стандартным пользователем."""
        login_page = LoginPage(page)
        login_page.open()
        login_page.login_as("standard_user", "secret_sauce")

        # После логина мы должны оказаться на странице товаров
        products_page = ProductsPage(page)
        products_page.should_be_opened()
        assert products_page.get_page_title() == products_page.PAGE_TITLE

    def test_locked_out_user(self, page):
        """Негативный тест: заблокированный пользователь."""
        login_page = LoginPage(page)
        login_page.open()
        login_page.login_as("locked_out_user", "secret_sauce")

        # Мы должны остаться на странице логина и увидеть ошибку
        assert login_page.is_error_displayed()
        assert login_page.get_error_message_text() == login_page.LOCKED_OUT_MESSAGE

    def test_invalid_credentials(self, page):
        """Негативный тест: неверный пароль."""
        login_page = LoginPage(page)
        login_page.open()
        login_page.login_as("standard_user", "wrong_password")

        assert login_page.is_error_displayed()
        assert login_page.get_error_message_text() == login_page.INVALID_CREDENTIALS_MESSAGE

    def test_empty_username(self, page):
        """Негативный тест: пустое имя пользователя."""
        login_page = LoginPage(page)
        login_page.open()
        login_page.enter_password("secret_sauce")
        login_page.click_login()

        assert login_page.is_error_displayed()
        assert login_page.get_error_message_text() == login_page.EMPTY_USERNAME_MESSAGE

    def test_empty_password(self, page):
        """Негативный тест: пустой пароль."""
        login_page = LoginPage(page)
        login_page.open()
        login_page.enter_username("standard_user")
        login_page.click_login()

        assert login_page.is_error_displayed()
        assert login_page.get_error_message_text() == login_page.EMPTY_PASSWORD_MESSAGE

    def test_logout(self, page):
        """Проверка выхода из системы."""
        # Логинимся
        login_page = LoginPage(page)
        login_page.open()
        login_page.login_as("standard_user", "secret_sauce")

        # Проверяем, что мы на странице товаров
        products_page = ProductsPage(page)
        products_page.should_be_opened()

        # Выходим
        products_page.logout()

        # Проверяем, что вернулись на страницу логина
        login_page.should_be_opened()