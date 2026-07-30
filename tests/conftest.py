import pytest
from playwright.sync_api import Page, BrowserContext, Browser
from datetime import datetime
import os
from utils.api_auth import ApiAuth
from config import settings


# ================== ФИКСТУРЫ ==================

@pytest.fixture(scope="function")
def context(browser: Browser) -> BrowserContext:
    context = browser.new_context(
        viewport={'width': 1920, 'height': 1080},
        locale='en-US'
    )
    yield context
    context.close()


@pytest.fixture(scope="function")
def page(context: BrowserContext) -> Page:
    page = context.new_page()
    yield page


@pytest.fixture(scope="function")
def logged_in_page(context: BrowserContext) -> Page:
    """Фикстура: возвращает уже залогиненную страницу."""
    page = context.new_page()
    ApiAuth.login_via_api(page, settings.LOGIN, settings.PASSWORD)
    yield page


# ================== ХУК ДЛЯ СКРИНШОТОВ ==================

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        page = item.funcargs.get('page', None) or item.funcargs.get('logged_in_page', None)

        if page is not None:
            screenshot_dir = os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                "screenshots"
            )
            os.makedirs(screenshot_dir, exist_ok=True)

            test_name = item.name.replace("/", "_").replace("::", "_")
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"{test_name}_{timestamp}.png"
            filepath = os.path.join(screenshot_dir, filename)

            page.screenshot(path=filepath, full_page=True)
            print(f"\n📸 СКРИНШОТ СОХРАНЁН: {filepath}")

            try:
                import allure
                allure.attach.file(
                    filepath,
                    name=f"Падение: {item.name}",
                    attachment_type=allure.attachment_type.PNG
                )
            except ImportError:
                pass
