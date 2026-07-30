import allure
from playwright.sync_api import Page


class ApiAuth:
    """
    Хелпер для логина через API/JavaScript.
    """

    @staticmethod
    def login_via_api(page: Page, username: str, password: str) -> None:
        """
        Логинимся, минуя UI.
        """
        with allure.step(f"🔑 Логинюсь через API: {username}"):
            page.goto("https://www.saucedemo.com", wait_until="domcontentloaded")

            # Правильный способ: передаём параметр как второй аргумент evaluate
            page.evaluate(
                """
                (user) => {
                    document.cookie = "session-username=" + user + "; path=/";
                }
                """,
                username  # ← передаётся как аргумент функции
            )

            page.goto("https://www.saucedemo.com/inventory.html", wait_until="domcontentloaded")