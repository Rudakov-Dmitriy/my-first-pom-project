import allure
from playwright.sync_api import Page, expect, TimeoutError as PlaywrightTimeoutError
import logging
import re
from typing import Optional

logger = logging.getLogger(__name__)


class BasePage:
    """
    Родительский класс для всех страниц.
    """

    def __init__(self, page: Page):
        self.page = page
        self.base_url = "https://www.saucedemo.com"
        self.default_timeout = 10000

    # ========== НАВИГАЦИЯ ==========

    def open(self, path: str = "") -> None:
        with allure.step(f"🌐 Открываю: {self.base_url}{path}"):
            full_url = f"{self.base_url}{path}"
            logger.info(f"🌐 Открываю: {full_url}")
            self.page.goto(full_url, wait_until='domcontentloaded')
        return self

    # ========== РАБОТА С ЭЛЕМЕНТАМИ ==========

    def click(self, selector: str, timeout: Optional[int] = None) -> None:
        timeout = timeout or self.default_timeout
        with allure.step(f"🖱️ Кликаю: {selector}"):
            logger.info(f"🖱️ Кликаю: {selector}")
            element = self.page.locator(selector)
            element.wait_for(state="visible", timeout=timeout)
            element.click()

    def fill(self, selector: str, text: str, timeout: Optional[int] = None) -> None:
        timeout = timeout or self.default_timeout
        with allure.step(f"⌨️ Заполняю '{selector}' значением: {text}"):
            logger.info(f"⌨️ Заполняю '{selector}' значением: {text}")
            element = self.page.locator(selector)
            element.wait_for(state="visible", timeout=timeout)
            element.fill(text)

    def get_text(self, selector: str, timeout: Optional[int] = None) -> str:
        timeout = timeout or self.default_timeout
        with allure.step(f"📝 Получаю текст: {selector}"):
            element = self.page.locator(selector)
            element.wait_for(state="attached", timeout=timeout)
            return element.inner_text()

    # ========== ПРОВЕРКИ ==========

    def should_be_visible(self, selector: str, timeout: Optional[int] = None) -> None:
        timeout = timeout or self.default_timeout
        with allure.step(f"👁️ Проверяю видимость: {selector}"):
            logger.info(f"👁️ Проверяю видимость: {selector}")
            expect(self.page.locator(selector)).to_be_visible(timeout=timeout)

    def should_have_text(self, selector: str, text: str, timeout: Optional[int] = None) -> None:
        timeout = timeout or self.default_timeout
        with allure.step(f"📝 Проверяю текст '{selector}' на содержание: {text}"):
            logger.info(f"📝 Проверяю текст '{selector}' на содержание: {text}")
            expect(self.page.locator(selector)).to_contain_text(text, timeout=timeout)

    def is_visible(self, selector: str, timeout: Optional[int] = None) -> bool:
        """
        Проверяет, видим ли элемент. Возвращает True/False, НЕ роняет тест.
        """
        timeout = timeout or self.default_timeout
        with allure.step(f"🔍 Проверяю наличие: {selector}"):
            try:
                self.page.locator(selector).wait_for(state="visible", timeout=timeout)
                return True
            except PlaywrightTimeoutError:
                return False

    # ========== ОЖИДАНИЯ ==========

    def wait_for_url(self, url_part: str, timeout: Optional[int] = None) -> None:
        timeout = timeout or self.default_timeout
        with allure.step(f"⏳ Жду URL: {url_part}"):
            logger.info(f"⏳ Жду URL, содержащий: {url_part}")
            expect(self.page).to_have_url(re.compile(f".*{url_part}.*"), timeout=timeout)

    # ========== СЛУЖЕБНЫЕ ==========

    def get_current_url(self) -> str:
        return self.page.url

    def get_title(self) -> str:
        return self.page.title()

    def take_screenshot(self, name: str = "screenshot") -> str:
        filepath = f"screenshots/{name}.png"
        self.page.screenshot(path=filepath, full_page=True)
        logger.info(f"📸 Скриншот сохранён: {filepath}")
        return filepath
