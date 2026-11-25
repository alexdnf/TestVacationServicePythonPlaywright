import requests


# Есть API POST /pay и POST /credit, которые отвечают за платеж картой и кредит соответственно
# требования такие же как для UI части
# 4444 4444 4444 4441 - успех, успешное уведомление
# 4444 4444 4444 4442 - карта отклонена, уведомление об ошибке, запись в базу DECLINED
# Случайный номер карты - отклонено, уведомление об ошибке (400)

def test_payment_api_approved_request(card_data_valid_number):
    base_url = "http://localhost:8080/api/v1"

    response = requests.post(
        url=f"{base_url}/pay",
        json=card_data_valid_number
    )
    assert response.status_code == 200

    response_json = response.json()
    assert response_json.get("status") == "APPROVED"

def test_credit_api_approved_requests(card_data_valid_number):
    base_url = "http://localhost:8080/api/v1"

    response = requests.post(
        url=f"{base_url}/credit",
        json=card_data_valid_number
    )

    assert response.status_code == 200

    response_json = response.json()
    assert response_json.get("status") == "APPROVED"

def test_payment_api_decline_request(card_data_blacklist_number):
    base_url = "http://localhost:8080/api/v1"

    response = requests.post(
        url=f"{base_url}/pay",
        json=card_data_blacklist_number
    )
    assert response.status_code == 200

    response_json = response.json()
    assert response_json.get("status") == "DECLINED"

def test_credit_api_decline_requests(card_data_blacklist_number):
    base_url = "http://localhost:8080/api/v1"

    response = requests.post(
        url=f"{base_url}/credit",
        json=card_data_blacklist_number
    )

    assert response.status_code == 200

    response_json = response.json()
    assert response_json.get("status") == "DECLINED"

def test_payment_api_400_random_card_request(card_data_random):
    base_url = "http://localhost:8080/api/v1"

    response = requests.post(
        url=f"{base_url}/pay",
        json=card_data_random
    )

    assert response.status_code == 400
    response_json = response.json()
    assert response_json.get("message") == "Invalid Value Provided"

def test_credit_api_400_random_card_requests(card_data_random):

    base_url = "http://localhost:8080/api/v1"
    response = requests.post(
        url=f"{base_url}/credit",
        json=card_data_random
    )

    assert response.status_code == 400
    response_json = response.json()
    assert response_json.get("message") == "Invalid Value Provided"