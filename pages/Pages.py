
from playwright.sync_api import Page, Locator


class MainPage:
    def __init__(self, page: Page):
        self.page = page

    def open(self):
        self.page.goto("http://localhost:8080/")


class CardFormPage:

    URL = "http://localhost:8080/"
    # --- Основные селекторы ---
    _INPUT_CONTROLS_SELECTOR = ".input__control"
    _HEADER_SELECTOR = ".heading"
    _ERROR_MESSAGE_FIELD_SELECTOR = ".input__sub"

    def __init__(self, page: Page):
        self.page = page
        self._input_controls: Locator = page.locator(self._INPUT_CONTROLS_SELECTOR)

        # Поля
        self.card_number_field = self._input_controls.nth(0)
        self.card_month_field = self._input_controls.nth(1)
        self.card_year_field = self._input_controls.nth(2)
        self.card_holder_field = self._input_controls.nth(3)
        self.card_cvc_field = self._input_controls.nth(4)


        # Сообщения об ошибках
       # self._error_messages: Locator = page.locator(self._ERROR_MESSAGE_FIELD_SELECTOR)


        # Заголовок и кнопка
        self.header = page.locator(self._HEADER_SELECTOR).nth(2)

        self.payment_button = page.get_by_role("button", name="Купить", exact=True)
        self.credit_button = page.get_by_role("button", name="Купить в кредит", exact=True)
        self.submit_button = page.get_by_role("button", name="Продолжить", exact=True)


        self.successful_notification = page.get_by_text("Операция одобрена Банком.", exact=True)
        self.decline_notification = page.get_by_text("Ошибка! Банк отказал в проведении операции.", exact=True)



    def open_payment_page(self):
        self.payment_button.click()

    def open_credit_page(self):
        self.credit_button.click()

    def fill_card_data(self, data: dict):
        self.card_number_field.fill(data["number"])
        self.card_month_field.fill(data["month"])
        self.card_year_field.fill(data["year"])
        self.card_holder_field.fill(data["holder"])
        self.card_cvc_field.fill(data["cvc"])

    def submit(self):
        self.submit_button.click()

    # def should_see_error_empty_form(self):
    #     expect(self._error_messages.nth(0)).to_have_text("Неверный формат")
    #     expect(self._error_messages.nth(1)).to_have_text("Неверный формат")
    #     expect(self._error_messages.nth(2)).to_have_text("Неверный формат")
    #     expect(self._error_messages.nth(3)).to_have_text("Поле обязательно для заполнения")
    #     expect(self._error_messages.nth(4)).to_have_text("Неверный формат")
    #
    # def should_see_error_invalid_number(self):
    #     expect(self._error_messages.nth(0)).to_have_text("Неверный формат")
    #
    # def should_see_error_invalid_month(self):
    #     expect(self._error_messages.nth(1)).to_have_text("Неверный формат")








