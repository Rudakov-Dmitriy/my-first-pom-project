import pytest
from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from pages.cart_page import CartPage
from config import settings


class TestCart:
    """Тесты корзины SauceDemo."""

    @pytest.fixture(autouse=True)
    def setup(self, page):
        """Перед каждым тестом — логинимся."""
        login_page = LoginPage(page)
        login_page.open()
        login_page.login_as(settings.LOGIN, settings.PASSWORD)
        self.products_page = ProductsPage(page)
        self.products_page.should_be_opened()

    def test_add_one_item_to_cart(self, page):
        """Добавить один товар в корзину и проверить."""
        # Запоминаем название ПЕРВОГО товара
        first_item_name = self.products_page.page.locator(
            self.products_page.product_names
        ).first.inner_text()

        # Добавляем первый товар
        self.products_page.add_product_to_cart(0)

        # Проверяем счётчик на иконке корзины
        assert self.products_page.get_cart_badge_count() == 1

        # Переходим в корзину
        cart_page = self.products_page.go_to_cart()
        cart_page.should_be_opened()

        # Проверяем, что товар в корзине
        assert cart_page.get_items_count() == 1
        assert cart_page.get_item_name(0) == first_item_name

    def test_add_multiple_items_to_cart(self, page):
        """Добавить несколько товаров и проверить корзину."""
        # Добавляем первый и второй товары
        self.products_page.add_product_to_cart(0)
        self.products_page.add_product_to_cart(1)

        # Проверяем счётчик
        assert self.products_page.get_cart_badge_count() == 2

        # Переходим в корзину
        cart_page = self.products_page.go_to_cart()
        cart_page.should_be_opened()

        # Проверяем количество
        assert cart_page.get_items_count() == 2

    def test_remove_item_from_cart(self, page):
        """Удалить товар из корзины."""
        # Добавляем товар и переходим в корзину
        self.products_page.add_product_to_cart(0)
        cart_page = self.products_page.go_to_cart()

        # Удаляем товар
        cart_page.remove_item(0)

        # Проверяем, что корзина пуста
        assert cart_page.get_items_count() == 0

    def test_empty_cart(self, page):
        """Перейти в пустую корзину и проверить."""
        cart_page = self.products_page.go_to_cart()
        cart_page.should_be_opened()

        # Корзина должна быть пустой
        assert cart_page.get_items_count() == 0