from pages.base_page import BasePage
from playwright.sync_api import Page


class ProductsPage(BasePage):
    """
    Страница с товарами (после успешного логина).
    """

    def __init__(self, page: Page):
        super().__init__(page)

        # Селекторы
        self.title = ".title"
        self.shopping_cart_link = ".shopping_cart_link"
        self.burger_menu = "#react-burger-menu-btn"
        self.logout_link = "#logout_sidebar_link"
        self.sort_dropdown = "[data-test='product-sort-container']"
        self.add_to_cart_buttons = ".btn_inventory"
        self.product_names = ".inventory_item_name"

        # Тексты
        self.PAGE_TITLE = "Products"

    def should_be_opened(self) -> None:
        """Проверяет, что мы на странице товаров."""
        self.wait_for_url("/inventory.html")
        self.should_have_text(self.title, self.PAGE_TITLE)

    def get_page_title(self) -> str:
        """Возвращает текст заголовка страницы."""
        return self.get_text(self.title)

    def logout(self) -> None:
        """Выход из системы через бургер-меню."""
        self.click(self.burger_menu)
        self.click(self.logout_link)

    def add_product_to_cart(self, index: int = 0) -> "ProductsPage":
        """
        Добавить товар в корзину по индексу.
        index=0 — первый товар, index=1 — второй.
        """
        buttons = self.page.locator(self.add_to_cart_buttons)
        buttons.nth(index).click()
        return self

    def get_product_count(self) -> int:
        """Количество товаров на странице."""
        return self.page.locator(self.product_names).count()

    def go_to_cart(self):
        """Перейти в корзину."""
        self.click(self.shopping_cart_link)
        # Здесь можно вернуть CartPage, но пока не будем усложнять