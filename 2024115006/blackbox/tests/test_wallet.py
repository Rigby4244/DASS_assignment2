import pytest
import requests

BASE_URL    = "http://localhost:8080/api/v1"
ROLL_NUMBER = "2024115006"
USER_ID     = "1"

def headers(roll=ROLL_NUMBER, user=USER_ID):
    h = {"X-Roll-Number": roll}
    if user is not None:
        h["X-User-ID"] = user
    return h

def admin_headers(roll=ROLL_NUMBER):
    return {"X-Roll-Number": roll}

def url(path):
    return f"{BASE_URL}{path}"

def test_get_wallet_returns_200():
    r = requests.get(url("/wallet"), headers=headers())
    assert r.status_code == 200

def test_add_money_valid():
    r = requests.post(url("/wallet/add"), json={"amount": 500}, headers=headers())
    assert r.status_code == 200

def test_add_zero_returns_400():
    r = requests.post(url("/wallet/add"), json={"amount": 0}, headers=headers())
    assert r.status_code == 400

def test_add_negative_returns_400():
    r = requests.post(url("/wallet/add"), json={"amount": -100}, headers=headers())
    assert r.status_code == 400

def test_add_above_100000_returns_400():
    r = requests.post(url("/wallet/add"), json={"amount": 100001}, headers=headers())
    assert r.status_code == 400

def test_add_exactly_100000_is_valid():
    r = requests.post(url("/wallet/add"), json={"amount": 100000}, headers=headers())
    assert r.status_code == 200

def test_pay_more_than_balance_returns_400():
    h = headers()
    r_wallet = requests.get(url("/wallet"), headers=h).json()
    if isinstance(r_wallet, list):
        wallet_data = r_wallet[0]
    else:
        wallet_data = r_wallet.get("wallet") or r_wallet
    balance = float(wallet_data.get("wallet_balance", 0))
    assert balance > 0
    overdraft_amount = balance + 500.0 
    r = requests.post(url("/wallet/pay"), json={"amount": overdraft_amount}, headers=h)
    assert r.status_code == 400

def test_pay_exact_amount_deducted():
    requests.post(url("/wallet/add"), json={"amount": 200}, headers=headers())
    before = float(requests.get(url("/wallet"), headers=headers()).json().get("balance", 0))
    requests.post(url("/wallet/pay"), json={"amount": 100}, headers=headers())
    after  = float(requests.get(url("/wallet"), headers=headers()).json().get("balance", 0))
    assert abs((before - after) - 100) < 0.01