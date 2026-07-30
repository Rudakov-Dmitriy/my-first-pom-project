from pages.base_page import BasePage
from playwright.sync_api import Page


class LoginPage(BasePage):
    """
    Страница логина SauceDemo.
    Содержит ТОЛЬКО то, что относится к странице логина.
    Никакой логики навигации на другие страницы (это делают тесты).
    """

    def __init__(self, page: Page):
        super().__init__(page)

        # ========== СЕЛЕКТОРЫ ==========
        # Храним ВСЕ селекторы здесь. Изменился дизайн? Меняем только тут.
        self.username_field = "#user-name"
        self.password_field = "#password"
        self.login_button = "#login-button"
        self.error_message = "[data-test='error']"
        self.error_button = ".error-button"

        # Текст ошибок (чтобы не хардкодить в тестах)
        self.LOCKED_OUT_MESSAGE = "Epic sadface: Sorry, this user has been locked out."
        self.INVALID_CREDENTIALS_MESSAGE = "Epic sadface: Username and password do not match any user in this service"
        self.EMPTY_USERNAME_MESSAGE = "Epic sadface: Username is required"
        self.EMPTY_PASSWORD_MESSAGE = "Epic sadface: Password is required"

    # ========== ДЕЙСТВИЯ ==========

    def open(self) -> "LoginPage":
        """Открыть страницу логина."""
        super().open("/")
        self.should_be_opened()  # Проверяем, что мы действительно на странице логина
        return self

    def enter_username(self, username: str) -> "LoginPage":
        """Ввести имя пользователя."""
        self.fill(self.username_field, username)
        return self

    def enter_password(self, password: str) -> "LoginPage":
        """Ввести пароль."""
        self.fill(self.password_field, password)
        return self

    def click_login(self):
        """
        Нажать кнопку Login.
        НЕ возвращает новую страницу, потому что:
        - При успехе — редирект на ProductsPage
        - При ошибке — остаёмся на LoginPage
        Пусть тест решает, что проверять.
        """
        self.click(self.login_button)

    def login_as(self, username: str, password: str) -> None:
        """
        Комбо-метод: логин в одно действие.
        Используй, когда не нужно проверять промежуточные шаги.
        """
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()

    # ========== ПРОВЕРКИ ==========

    def should_be_opened(self) -> None:
        """Проверяет, что страница логина открыта."""
        self.should_be_visible(self.login_button, timeout=5000)
        self.should_be_visible(self.username_field)

    def get_error_message_text(self) -> str:
        """Получить текст ошибки."""
        return self.get_text(self.error_message)

    def is_error_displayed(self) -> bool:
        """Проверяет, отображается ли сообщение об ошибке."""
        return self.is_visible(self.error_message)

    def close_error(self) -> "LoginPage":
        """Закрыть сообщение об ошибке (нажать на крестик)."""
        if self.is_error_displayed():
            self.click(self.error_button)
        return self

    def clear_fields(self) -> "LoginPage":
        """Очистить поля ввода."""
        self.fill(self.username_field, "")
        self.fill(self.password_field, "")
        return self