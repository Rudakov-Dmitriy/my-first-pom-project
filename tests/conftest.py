import pytest
from playwright.sync_api import Page, BrowserContext, Browser
from datetime import datetime
import os


# ================== ФИКСТУРЫ ==================

@pytest.fixture(scope="function")
def context(browser: Browser) -> BrowserContext:
    """
    Создаёт чистый контекст для каждого теста.
    browser — встроенная фикстура pytest-playwright.
    """
    context = browser.new_context(
        viewport={'width': 1920, 'height': 1080},
        locale='ru-RU'  # Русская локаль для наших сайтов
    )
    yield context
    context.close()


@pytest.fixture(scope="function")
def page(context: BrowserContext) -> Page:
    """Открывает новую страницу."""
    page = context.new_page()
    yield page


# ================== ХУК ДЛЯ СКРИНШОТОВ ==================

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Скриншот при падении теста. Совместим с pytest 9.x"""

    # Даём тесту выполниться
    outcome = yield
    report = outcome.get_result()

    # Только фаза выполнения теста (не setup/teardown) и только если тест упал
    if report.when == "call" and report.failed:

        # Достаём page. В pytest 9 funcargs работает так же
        page = item.funcargs.get('page', None)

        if page is not None:
            # Папка для скриншотов в корне проекта
            screenshot_dir = os.path.join(
                os.path.dirname(os.path.dirname(__file__)),  # Поднимаемся из tests/ в корень
                "screenshots"
            )
            os.makedirs(screenshot_dir, exist_ok=True)

            # Имя файла
            test_name = item.name.replace("/", "_").replace("::", "_")
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"{test_name}_{timestamp}.png"
            filepath = os.path.join(screenshot_dir, filename)

            # Делаем скриншот
            page.screenshot(path=filepath, full_page=True)
            print(f"\n📸 СКРИНШОТ СОХРАНЁН: {filepath}")

            # Прикрепляем к Allure (если установлен)
            try:
                import allure
                allure.attach.file(
                    filepath,
                    name=f"Падение: {item.name}",
                    attachment_type=allure.attachment_type.PNG
                )
            except ImportError:
                pass  # Allure не установлен — и ладно