import pytest
from playwright.sync_api import Page, expect

from data.SQL_Helper import SQLHelper
from pages.Pages import CardFormPage, MainPage
from tests.conftest import card_data_valid_number


# Данные для теста:
# 4444 4444 4444 4441 - успех, успешное уведомление и запись в базу APPROVED
# 4444 4444 4444 4442 - карта отклонена, уведомление об ошибке, запись в базу DECLINED
# Случайный номер карты - отклонено, уведомление об ошибке

def test_main_page_is_opened(page: Page):
    MainPage(page).open()
    main_page = MainPage(page)
    expect(main_page.main_header).to_be_visible()

def test_payment_valid_card_data(page: Page, card_data_valid_number):

    MainPage(page).open()
    main_page = MainPage(page)
    expect(main_page.main_header).to_be_visible()
    payment_page = CardFormPage(page)
    payment_page.open_payment_page()
    expect(payment_page.header).to_have_text("Оплата по карте")
    payment_page.fill_card_data(card_data_valid_number)
    payment_page.submit()
    expect(payment_page.successful_notification).to_be_visible(timeout=15000)
    status = SQLHelper.get_status_payment()
    amount_payment = SQLHelper.get_amount_payment()
    assert status == "APPROVED"
    assert amount_payment == 4500000


def test_credit_valid_card_data(page: Page, card_data_valid_number):

    MainPage(page).open()
    main_page = MainPage(page)
    expect(main_page.main_header).to_be_visible()
    credit_page = CardFormPage(page)
    credit_page.open_credit_page()
    expect(credit_page.header).to_have_text("Кредит по данным карты")
    credit_page.fill_card_data(card_data_valid_number)
    credit_page.submit()
    expect(credit_page.successful_notification).to_be_visible(timeout=15000)
    status = SQLHelper.get_status_credit()
    assert status == "APPROVED"

def test_payment_blacklist_card(page: Page, card_data_blacklist_number):

    MainPage(page).open()
    main_page = MainPage(page)
    expect(main_page.main_header).to_be_visible()
    payment_page = CardFormPage(page)
    payment_page.open_payment_page()
    expect(payment_page.header).to_have_text("Оплата по карте")
    payment_page.fill_card_data(card_data_blacklist_number)
    payment_page.submit()
    expect(payment_page.decline_notification).to_be_visible(timeout=15000)
    status = SQLHelper.get_status_payment()
    assert status == "DECLINED"

def test_credit_blacklist_card(page: Page, card_data_blacklist_number):
    MainPage(page).open()
    main_page = MainPage(page)
    expect(main_page.main_header).to_be_visible()
    credit_page = CardFormPage(page)
    credit_page.open_credit_page()
    credit_page.fill_card_data(card_data_blacklist_number)
    credit_page.submit()
    expect(credit_page.decline_notification).to_be_visible(timeout=15000)
    status = SQLHelper.get_status_payment()
    assert status == "DECLINED"


def test_payment_random_decline_card(page: Page, card_data_random):
    MainPage(page).open()
    main_page = MainPage(page)
    expect(main_page.main_header).to_be_visible()
    payment_page = CardFormPage(page)
    payment_page.open_payment_page()
    payment_page.fill_card_data(card_data_random)
    payment_page.submit()
    expect(payment_page.decline_notification).to_be_visible(timeout=15000)


def test_credit_random_decline_card(page: Page, card_data_random):
    MainPage(page).open()
    main_page = MainPage(page)
    expect(main_page.main_header).to_be_visible()
    payment_page = CardFormPage(page)
    payment_page.open_credit_page()
    payment_page.fill_card_data(card_data_random)
    payment_page.submit()
    expect(payment_page.decline_notification).to_be_visible(timeout=15000)


def test_send_payment_empty_form(page: Page):
    MainPage(page).open()
    main_page = MainPage(page)
    expect(main_page.main_header).to_be_visible()
    payment_page = CardFormPage(page)
    payment_page.open_payment_page()
    payment_page.submit()
    expect(payment_page.card_number_field_error).to_be_visible()
    expect(payment_page.card_number_field_error).to_have_text("Неверный формат")
    expect(payment_page.month_field_error).to_be_visible()
    expect(payment_page.month_field_error).to_have_text("Неверный формат")
    expect(payment_page.year_field_error).to_be_visible()
    expect(payment_page.year_field_error).to_have_text("Неверный формат")
    expect(payment_page.card_holder_field_error).to_be_visible()
    expect(payment_page.card_holder_field_error).to_have_text("Поле обязательно для заполнения")
    expect(payment_page.cvc_field_error).to_be_visible()
    expect(payment_page.cvc_field_error).to_have_text("Неверный формат")


# @pytest.mark.parametrize(
#     "missing_field, expected_error",
#     [
#         ("number", "Неверный формат"),
#         ("month",  "Неверный формат"),
#         ("year",   "Неверный формат"),
#         ("holder", "Поле обязательно для заполнения"),
#         ("cvc",    "Неверный формат"),
#     ],
# )
# def test_payment_missing_field(page, card_data_valid_number, missing_field, expected_error):
#     MainPage(page).open()
#     main_page = MainPage(page)
#     expect(main_page.main_header).to_be_visible()
#
#     payment_page = CardFormPage(page)
#     payment_page.open_payment_page()
#     expect(payment_page.header).to_have_text("Оплата по карте")
#
#     payment_page.fill_card_data(card_data_valid_number(exclude=missing_field))
#     payment_page.submit()
#     expect(payment_page.card_holder_field_error).to_have_text(expected_error)





