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

def test_get_loyalty_returns_200():
    r = requests.get(url("/loyalty"), headers=headers())
    assert r.status_code == 200

def test_redeem_zero_returns_400():
    r = requests.post(url("/loyalty/redeem"), json={"points": 0}, headers=headers())
    assert r.status_code == 400

def test_redeem_more_than_available_returns_400():
    points = requests.get(url("/loyalty"), headers=headers()).json().get("points", 0)
    r = requests.post(url("/loyalty/redeem"), json={"points": points + 9999}, headers=headers())
    assert r.status_code == 400
