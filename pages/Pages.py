
from playwright.sync_api import Page, Locator, expect


class MainPage:
    def __init__(self, page: Page):
        self.page = page

        self.main_header = self.page.locator(".heading", has_text="Путешествие дня")

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

        self._input__subs: Locator = page.locator(self._ERROR_MESSAGE_FIELD_SELECTOR)

        self.card_number_field_error = self._input__subs.nth(0)
        self.month_field_error = self._input__subs.nth(1)
        self.year_field_error = self._input__subs.nth(2)
        self.card_holder_field_error = self._input__subs.nth(3)
        self.cvc_field_error = self._input__subs.nth(4)



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
        if "number" in data:
            self.card_number_field.fill(data["number"])
        if "month" in data:
            self.card_month_field.fill(data["month"])
        if "year" in data:
            self.card_year_field.fill(data["year"])
        if "holder" in data:
            self.card_holder_field.fill(data["holder"])
        if "cvc" in data:
            self.card_cvc_field.fill(data["cvc"])

    # def error_for(self, field: str):
    #     locators = {
    #         "number": self.card_number_field_error,
    #         "month": self.month_field_error,
    #         "year": self.year_field_error,
    #         "holder": self.card_holder_field_error,
    #         "cvc": self.cvc_field_error,
    #     }
    #     return locators[field]

    def submit(self):
        self.submit_button.click()









