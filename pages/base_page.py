from playwright.sync_api import Page, expect, TimeoutError as PlaywrightTimeoutError
import logging
import re
from typing import Optional

# Настраиваем логгер — будем видеть в консоли, что делает наш фреймворк
logger = logging.getLogger(__name__)


class BasePage:
    """
    Родительский класс для всех страниц.
    Содержит методы, которые нужны на КАЖДОЙ странице.
    Не содержит селекторов конкретных страниц.
    """

    def __init__(self, page: Page):
        self.page = page
        self.base_url = "https://www.saucedemo.com"  # Поменяем на наш тестовый сайт
        self.default_timeout = 10000  # 10 секунд (Playwright работает в миллисекундах)

    # ========== НАВИГАЦИЯ ==========

    def open(self, path: str = "") -> None:
        """
        Открывает страницу по URL.
        wait_until='domcontentloaded' — ждём загрузки DOM, но не ждём картинки.
        Это быстрее, чем 'load', и надёжнее, чем 'commit'.
        """
        full_url = f"{self.base_url}{path}"
        logger.info(f"🌐 Открываю: {full_url}")
        self.page.goto(full_url, wait_until='domcontentloaded')
        return self  # Возвращаем self для цепочки вызовов (method chaining)

    # ========== РАБОТА С ЭЛЕМЕНТАМИ ==========

    def locator(self, selector: str):
        """
        Возвращает локатор. Не ждёт, не проверяет — просто локатор.
        Playwright сам делает автоожидания при действиях (click, fill).
        """
        return self.page.locator(selector)

    def click(self, selector: str, timeout: Optional[int] = None) -> None:
        """
        Клик по элементу с гарантией, что он видим и доступен.
        Playwright автоматически ждёт, пока элемент станет видимым и enabled.
        """
        timeout = timeout or self.default_timeout
        logger.info(f"🖱️ Кликаю: {selector}")
        element = self.page.locator(selector)
        element.wait_for(state="visible", timeout=timeout)
        element.click()

    def fill(self, selector: str, text: str, timeout: Optional[int] = None) -> None:
        """
        Заполняет поле ввода.
        fill() в Playwright САМ очищает поле перед вводом (в отличие от Selenium type).
        """
        timeout = timeout or self.default_timeout
        logger.info(f"⌨️ Заполняю '{selector}' значением: {text}")
        element = self.page.locator(selector)
        element.wait_for(state="visible", timeout=timeout)
        element.fill(text)

    def get_text(self, selector: str, timeout: Optional[int] = None) -> str:
        """
        Получает текст элемента.
        wait_for('attached') — элемент должен быть в DOM, но не обязательно видим.
        """
        timeout = timeout or self.default_timeout
        element = self.page.locator(selector)
        element.wait_for(state="attached", timeout=timeout)
        return element.inner_text()

    # ========== ПРОВЕРКИ ==========

    def is_visible(self, selector: str, timeout: Optional[int] = None) -> bool:
        """
        Проверяет, видим ли элемент на странице.
        Возвращает True/False, НЕ роняет тест.
        """
        timeout = timeout or self.default_timeout
        try:
            self.page.locator(selector).wait_for(state="visible", timeout=timeout)
            return True
        except PlaywrightTimeoutError:
            return False

    def should_be_visible(self, selector: str, timeout: Optional[int] = None) -> None:
        """
        Проверяет, что элемент видим. Если нет — РОНЯЕТ тест с AssertionError.
        Использует expect из Playwright — это даёт крутые сообщения об ошибках.
        """
        timeout = timeout or self.default_timeout
        logger.info(f"👁️ Проверяю видимость: {selector}")
        expect(self.page.locator(selector)).to_be_visible(timeout=timeout)

    def should_have_text(self, selector: str, text: str, timeout: Optional[int] = None) -> None:
        """
        Проверяет, что элемент содержит указанный текст.
        """
        timeout = timeout or self.default_timeout
        logger.info(f"📝 Проверяю текст '{selector}' на содержание: {text}")
        expect(self.page.locator(selector)).to_contain_text(text, timeout=timeout)

    # ========== ОЖИДАНИЯ ==========

    def wait_for_url(self, url_part: str, timeout: Optional[int] = None) -> None:
        """
        Ждёт, пока URL страницы будет содержать указанную строку.
        Полезно для проверки редиректов после логина.
        """
        timeout = timeout or self.default_timeout
        logger.info(f"⏳ Жду URL, содержащий: {url_part}")
        # Используем регулярное выражение вместо glob-паттерна
        # .* означает "любые символы до и после"
        expect(self.page).to_have_url(re.compile(f".*{url_part}.*"), timeout=timeout)

    # ========== СЛУЖЕБНЫЕ ==========

    def get_current_url(self) -> str:
        """Возвращает текущий URL страницы."""
        return self.page.url

    def get_title(self) -> str:
        """Возвращает title страницы."""
        return self.page.title()

    def take_screenshot(self, name: str = "screenshot") -> str:
        """
        Делает скриншот и возвращает путь к файлу.
        """
        filepath = f"screenshots/{name}.png"
        self.page.screenshot(path=filepath, full_page=True)
        logger.info(f"📸 Скриншот сохранён: {filepath}")
        return filepath