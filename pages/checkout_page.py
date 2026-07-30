import allure
from pages.base_page import BasePage
from playwright.sync_api import Page


class CheckoutPage(BasePage):
    """
    Страница оформления заказа (оба шага).
    """

    # Константы
    STEP_ONE_TITLE = "Checkout: Your Information"
    STEP_TWO_TITLE = "Checkout: Overview"
    COMPLETE_TITLE = "Checkout: Complete!"
    COMPLETE_HEADER = "Thank you for your order!"

    def __init__(self, page: Page):
        super().__init__(page)

        # Общий селектор заголовка
        self.title = ".title"

        # Шаг 1: форма
        self.first_name_field = "#first-name"
        self.last_name_field = "#last-name"
        self.postal_code_field = "#postal-code"
        self.continue_button = "#continue"
        self.cancel_button = "#cancel"
        self.error_message = "[data-test='error']"

        # Шаг 2: обзор
        self.finish_button = "#finish"
        self.subtotal_label = ".summary_subtotal_label"
        self.tax_label = ".summary_tax_label"
        self.total_label = ".summary_total_label"
        self.cart_items = ".cart_item"

        # Завершение
        self.complete_header = ".complete-header"
        self.complete_text = ".complete-text"
        self.back_home_button = "#back-to-products"

    # ========== Шаг 1: форма ==========

    def should_be_opened_step_one(self) -> None:
        with allure.step("👁️ Проверяю, что открыт шаг 1 оформления"):
            self.wait_for_url("/checkout-step-one.html")
            self.should_have_text(self.title, self.STEP_ONE_TITLE)

    def fill_checkout_form(self, first_name: str, last_name: str, postal_code: str) -> "CheckoutPage":
        with allure.step(f"📝 Заполняю форму: {first_name}, {last_name}, {postal_code}"):
            self.fill(self.first_name_field, first_name)
            self.fill(self.last_name_field, last_name)
            self.fill(self.postal_code_field, postal_code)
        return self

    def click_continue(self) -> None:
        with allure.step("➡️ Нажимаю Continue"):
            self.click(self.continue_button)

    def go_to_step_two(self, first_name: str, last_name: str, postal_code: str) -> None:
        with allure.step("📦 Перехожу ко второму шагу оформления"):
            self.fill_checkout_form(first_name, last_name, postal_code)
            self.click_continue()

    def get_error_message_text(self) -> str:
        return self.get_text(self.error_message)

    def is_error_displayed(self) -> bool:
        return self.is_visible(self.error_message)

    # ========== Шаг 2: обзор ==========

    def should_be_opened_step_two(self) -> None:
        with allure.step("👁️ Проверяю, что открыт шаг 2 оформления"):
            self.wait_for_url("/checkout-step-two.html")
            self.should_have_text(self.title, self.STEP_TWO_TITLE)

    def get_items_count(self) -> int:
        with allure.step("🔢 Считаю товары в заказе"):
            return self.page.locator(self.cart_items).count()

    def get_total_price(self) -> str:
        with allure.step("💰 Получаю итоговую сумму"):
            return self.get_text(self.total_label)

    def click_finish(self) -> None:
        with allure.step("✅ Нажимаю Finish"):
            self.click(self.finish_button)

    # ========== Завершение ==========

    def should_be_completed(self) -> None:
        with allure.step("🎉 Проверяю, что заказ оформлен"):
            self.wait_for_url("/checkout-complete.html")
            self.should_have_text(self.complete_header, self.COMPLETE_HEADER)

    def get_complete_message(self) -> str:
        return self.get_text(self.complete_header)

    def back_to_products(self) -> None:
        with allure.step("🔙 Возвращаюсь к товарам"):
            self.click(self.back_home_button)