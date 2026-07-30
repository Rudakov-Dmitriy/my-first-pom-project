import pytest
from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from config import settings


class TestLogin:
    """Тесты страницы логина SauceDemo."""

    @pytest.mark.smoke
    @pytest.mark.regression
    def test_successful_login(self, page):
        """Позитивный тест: логин со стандартным пользователем."""
        login_page = LoginPage(page)
        login_page.open()
        login_page.login_as(settings.LOGIN, settings.PASSWORD)

        products_page = ProductsPage(page)
        products_page.should_be_opened()
        assert products_page.get_page_title() == products_page.PAGE_TITLE

    @pytest.mark.regression
    @pytest.mark.parametrize("username,password,expected_error", [
        ("locked_out_user", "secret_sauce", LoginPage.LOCKED_OUT_MESSAGE),
        (settings.LOGIN, "wrong_password", LoginPage.INVALID_CREDENTIALS_MESSAGE),
        ("", settings.PASSWORD, LoginPage.EMPTY_USERNAME_MESSAGE),
        (settings.LOGIN, "", LoginPage.EMPTY_PASSWORD_MESSAGE),
    ])
    def test_login_errors(self, page, username, password, expected_error):
        """Параметризованный тест: проверка ошибок логина."""
        login_page = LoginPage(page)
        login_page.open()
        login_page.login_as(username, password)

        assert login_page.is_error_displayed()
        assert login_page.get_error_message_text() == expected_error

    @pytest.mark.smoke
    @pytest.mark.regression
    def test_logout(self, page):
        """Проверка выхода из системы."""
        login_page = LoginPage(page)
        login_page.open()
        login_page.login_as(settings.LOGIN, settings.PASSWORD)

        products_page = ProductsPage(page)
        products_page.should_be_opened()

        products_page.logout()

        login_page.should_be_opened()