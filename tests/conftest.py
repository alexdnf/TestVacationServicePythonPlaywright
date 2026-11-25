# docker-compose up --build
# java "-Dspring.datasource.url=jdbc:mysql://localhost:3306/app" -jar artifacts/aqa-shop.jar


import os

import pytest
from faker import Faker
from playwright.sync_api import sync_playwright


@pytest.fixture(scope="session")
def browser():
    # По умолчанию браузер видимый (удобно для демонстрации).
    # Для CI: HEADLESS=true pytest
    headless = os.getenv("HEADLESS", "true").lower() == "true"
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        yield browser
        browser.close()


@pytest.fixture
def context(browser):
    ctx = browser.new_context()
    yield ctx
    ctx.close()


@pytest.fixture
def page(context):
    yield context.new_page()

@pytest.fixture
def fake():
    return Faker()


@pytest.fixture
def card_data_valid_number(fake) -> dict[str, str]:
    # срок действия: от сегодня до +5 лет
    expire = fake.credit_card_expire(start="now", end="+5y", date_format="%m/%y")
    month, year = expire.split("/")

    return {
        "number": "4444 4444 4444 4441",
        "month": month,                # "09"
        "year": year,                  # "28"
        "holder": fake.name().upper(), # "IVAN PETROV"
        "cvc": fake.credit_card_security_code(),
    }

@pytest.fixture
def card_data_blacklist_number(fake) -> dict[str, str]:
    # срок действия: от сегодня до +5 лет
    expire = fake.credit_card_expire(start="now", end="+5y", date_format="%m/%y")
    month, year = expire.split("/")

    return {
        "number": "4444 4444 4444 4442",
        "month": month,                # "09"
        "year": year,                  # "28"
        "holder": fake.name().upper(), # "IVAN PETROV"
        "cvc": fake.credit_card_security_code(),
    }

@pytest.fixture
def card_data_random(fake) -> dict[str, str]:
    # срок действия: от сегодня до +5 лет
    expire = fake.credit_card_expire(start="now", end="+5y", date_format="%m/%y")
    month, year = expire.split("/")

    return {
        "number": fake.credit_card_number(),
        "month": month,                # "09"
        "year": year,                  # "28"
        "holder": fake.name().upper(), # "IVAN PETROV"
        "cvc": fake.credit_card_security_code(),
    }