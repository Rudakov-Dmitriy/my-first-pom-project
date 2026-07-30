import allure
from pages.base_page import BasePage
from playwright.sync_api import Page


class CartPage(BasePage):
    """
    Страница корзины SauceDemo.
    """

    PAGE_TITLE = "Your Cart"

    def __init__(self, page: Page):
        super().__init__(page)

        self.title = ".title"
        self.cart_items = ".cart_item"
        self.item_names = ".inventory_item_name"
        self.item_prices = ".inventory_item_price"
        self.remove_buttons = ".cart_button"
        self.continue_shopping_button = "#continue-shopping"
        self.checkout_button = "#checkout"

    def should_be_opened(self) -> None:
        with allure.step("👁️ Проверяю, что страница корзины открыта"):
            self.wait_for_url("/cart.html")
            self.should_have_text(self.title, self.PAGE_TITLE)

    def get_items_count(self) -> int:
        with allure.step("🔢 Считаю товары в корзине"):
            count = self.page.locator(self.cart_items).count()
            allure.attach(str(count), "Товаров в корзине", allure.attachment_type.TEXT)
            return count

    def get_item_name(self, index: int = 0) -> str:
        with allure.step(f"📝 Получаю название товара №{index + 1}"):
            name = self.page.locator(self.item_names).nth(index).inner_text()
            allure.attach(name, "Название товара", allure.attachment_type.TEXT)
            return name

    def remove_item(self, index: int = 0) -> "CartPage":
        with allure.step(f"🗑️ Удаляю товар №{index + 1} из корзины"):
            self.page.locator(self.remove_buttons).nth(index).click()
        return self

    def go_to_checkout(self):
        with allure.step("📦 Перехожу к оформлению заказа"):
            self.click(self.checkout_button)
            from pages.checkout_page import CheckoutPage
            return CheckoutPage(self.page)

    def continue_shopping(self) -> None:
        with allure.step("🔙 Возвращаюсь к покупкам"):
            self.click(self.continue_shopping_button)
