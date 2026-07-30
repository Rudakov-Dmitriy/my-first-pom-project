import pytest
from pages.products_page import ProductsPage


class TestCheckout:
    """Тесты оформления заказа."""

    @pytest.fixture(autouse=True)
    def setup(self, logged_in_page):
        """Используем быстрый логин через API и добавляем товар."""
        self.page = logged_in_page
        self.products_page = ProductsPage(self.page)
        self.products_page.should_be_opened()
        self.products_page.add_product_to_cart(0)

    @pytest.mark.smoke
    @pytest.mark.regression
    def test_successful_checkout(self):
        """Полный успешный цикл оформления заказа."""
        cart_page = self.products_page.go_to_cart()
        cart_page.should_be_opened()

        checkout_page = cart_page.go_to_checkout()
        checkout_page.should_be_opened_step_one()

        checkout_page.go_to_step_two("Dmitriy", "Rudakov", "123456")
        checkout_page.should_be_opened_step_two()
        assert checkout_page.get_items_count() == 1

        checkout_page.click_finish()
        checkout_page.should_be_completed()
        assert checkout_page.get_complete_message() == checkout_page.COMPLETE_HEADER

    @pytest.mark.regression
    def test_empty_first_name(self):
        """Ошибка: пустое имя."""
        cart_page = self.products_page.go_to_cart()
        checkout_page = cart_page.go_to_checkout()
        checkout_page.should_be_opened_step_one()

        checkout_page.fill_checkout_form("", "Rudakov", "123456")
        checkout_page.click_continue()

        assert checkout_page.is_error_displayed()
        assert "First Name" in checkout_page.get_error_message_text()

    @pytest.mark.regression
    def test_empty_last_name(self):
        """Ошибка: пустая фамилия."""
        cart_page = self.products_page.go_to_cart()
        checkout_page = cart_page.go_to_checkout()
        checkout_page.should_be_opened_step_one()

        checkout_page.fill_checkout_form("Dmitriy", "", "123456")
        checkout_page.click_continue()

        assert checkout_page.is_error_displayed()
        assert "Last Name" in checkout_page.get_error_message_text()

    @pytest.mark.regression
    def test_empty_postal_code(self):
        """Ошибка: пустой индекс."""
        cart_page = self.products_page.go_to_cart()
        checkout_page = cart_page.go_to_checkout()
        checkout_page.should_be_opened_step_one()

        checkout_page.fill_checkout_form("Dmitriy", "Rudakov", "")
        checkout_page.click_continue()

        assert checkout_page.is_error_displayed()
        assert "Postal Code" in checkout_page.get_error_message_text()
