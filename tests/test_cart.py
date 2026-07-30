import pytest
from pages.products_page import ProductsPage
from config import settings


class TestCart:
    """Тесты корзины SauceDemo."""

    @pytest.fixture(autouse=True)
    def setup(self, logged_in_page):
        """Используем быстрый логин через API."""
        self.page = logged_in_page
        self.products_page = ProductsPage(self.page)
        self.products_page.should_be_opened()

    @pytest.mark.smoke
    @pytest.mark.regression
    def test_add_one_item_to_cart(self):
        """Добавить один товар в корзину и проверить."""
        first_item_name = self.page.locator(
            self.products_page.product_names
        ).first.inner_text()

        self.products_page.add_product_to_cart(0)
        assert self.products_page.get_cart_badge_count() == 1

        cart_page = self.products_page.go_to_cart()
        cart_page.should_be_opened()

        assert cart_page.get_items_count() == 1
        assert cart_page.get_item_name(0) == first_item_name

    @pytest.mark.regression
    def test_add_multiple_items_to_cart(self):
        """Добавить несколько товаров и проверить корзину."""
        self.products_page.add_product_to_cart(0)
        self.products_page.add_product_to_cart(1)

        assert self.products_page.get_cart_badge_count() == 2

        cart_page = self.products_page.go_to_cart()
        cart_page.should_be_opened()

        assert cart_page.get_items_count() == 2

    @pytest.mark.regression
    def test_remove_item_from_cart(self):
        """Удалить товар из корзины."""
        self.products_page.add_product_to_cart(0)
        cart_page = self.products_page.go_to_cart()
        cart_page.remove_item(0)

        assert cart_page.get_items_count() == 0

    @pytest.mark.regression
    def test_empty_cart(self):
        """Перейти в пустую корзину и проверить."""
        cart_page = self.products_page.go_to_cart()
        cart_page.should_be_opened()

        assert cart_page.get_items_count() == 0