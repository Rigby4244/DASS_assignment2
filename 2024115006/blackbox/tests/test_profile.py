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

def test_get_profile_returns_200():
    r = requests.get(url("/profile"), headers=headers())
    assert r.status_code == 200

def test_update_profile_valid():
    payload = {"name": "Test User", "phone": "9876543210"}
    r = requests.put(url("/profile"), json=payload, headers=headers())
    assert r.status_code == 200

def test_update_profile_name_too_short_returns_400():
    r = requests.put(url("/profile"), json={"name": "A", "phone": "9876543210"}, headers=headers())
    assert r.status_code == 400

def test_update_profile_name_too_long_returns_400():
    r = requests.put(url("/profile"), json={"name": "A" * 51, "phone": "9876543210"}, headers=headers())
    assert r.status_code == 400

def test_update_profile_phone_not_10_digits_returns_400():
    r = requests.put(url("/profile"), json={"name": "Valid Name", "phone": "12345"}, headers=headers())
    assert r.status_code == 400

def test_update_profile_phone_with_letters_returns_400():
    r = requests.put(url("/profile"), json={"name": "Valid Name", "phone": "98765ABCDE"}, headers=headers())
    assert r.status_code == 400