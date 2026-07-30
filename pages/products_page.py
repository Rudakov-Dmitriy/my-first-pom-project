import allure
from pages.base_page import BasePage
from playwright.sync_api import Page


class ProductsPage(BasePage):
    """
    Страница с товарами (после успешного логина).
    """

    PAGE_TITLE = "Products"

    def __init__(self, page: Page):
        super().__init__(page)

        self.title = ".title"
        self.shopping_cart_link = ".shopping_cart_link"
        self.burger_menu = "#react-burger-menu-btn"
        self.logout_link = "#logout_sidebar_link"
        self.add_to_cart_buttons = ".btn_inventory"
        self.product_names = ".inventory_item_name"

    def should_be_opened(self) -> None:
        with allure.step("👁️ Проверяю, что страница товаров открыта"):
            self.wait_for_url("/inventory.html")
            self.should_have_text(self.title, self.PAGE_TITLE)

    def get_page_title(self) -> str:
        return self.get_text(self.title)

    def logout(self) -> None:
        with allure.step("🚪 Выхожу из системы"):
            self.click(self.burger_menu)
            self.click(self.logout_link)

    def add_product_to_cart(self, index: int = 0) -> "ProductsPage":
        with allure.step(f"🛒 Добавляю товар №{index + 1} в корзину"):
            buttons = self.page.locator(self.add_to_cart_buttons)
            buttons.nth(index).click()
        return self

    def get_cart_badge_count(self) -> int:
        with allure.step("🔢 Проверяю счётчик корзины"):
            try:
                badge = self.page.locator(".shopping_cart_badge")
                if badge.is_visible():
                    count = int(badge.inner_text())
                    allure.attach(str(count), "Количество в корзине", allure.attachment_type.TEXT)
                    return count
                return 0
            except Exception:
                return 0

    def go_to_cart(self):
        with allure.step("🛒 Перехожу в корзину"):
            self.click(self.shopping_cart_link)
            from pages.cart_page import CartPage
            return CartPage(self.page)
