from pages.base_page import BasePage
from playwright.sync_api import Page


class CartPage(BasePage):
    """
    Страница корзины SauceDemo.
    """

    # ========== КОНСТАНТЫ ==========
    PAGE_TITLE = "Your Cart"

    def __init__(self, page: Page):
        super().__init__(page)

        # ========== СЕЛЕКТОРЫ ==========
        self.title = ".title"
        self.cart_items = ".cart_item"
        self.item_names = ".inventory_item_name"
        self.item_prices = ".inventory_item_price"
        self.item_quantities = ".cart_quantity"
        self.remove_buttons = ".cart_button"
        self.continue_shopping_button = "#continue-shopping"
        self.checkout_button = "#checkout"

    # ========== ПРОВЕРКИ ==========

    def should_be_opened(self) -> None:
        """Проверить, что страница корзины открыта."""
        self.wait_for_url("/cart.html")
        self.should_have_text(self.title, self.PAGE_TITLE)

    # ========== ДЕЙСТВИЯ ==========

    def get_items_count(self) -> int:
        """Количество товаров в корзине."""
        return self.page.locator(self.cart_items).count()

    def get_item_name(self, index: int = 0) -> str:
        """Название товара по индексу."""
        return self.page.locator(self.item_names).nth(index).inner_text()

    def get_item_price(self, index: int = 0) -> str:
        """Цена товара по индексу."""
        return self.page.locator(self.item_prices).nth(index).inner_text()

    def remove_item(self, index: int = 0) -> "CartPage":
        """Удалить товар из корзины по индексу."""
        self.page.locator(self.remove_buttons).nth(index).click()
        return self

    def continue_shopping(self) -> None:
        """Вернуться к покупкам."""
        self.click(self.continue_shopping_button)

    def go_to_checkout(self) -> None:
        """Перейти к оформлению заказа."""
        self.click(self.checkout_button)