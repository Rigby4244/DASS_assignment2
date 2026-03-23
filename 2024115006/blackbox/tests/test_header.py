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

def test_missing_roll_number_returns_401():
    r = requests.get(url("/profile"), headers={"X-User-ID": USER_ID})
    assert r.status_code == 401

def test_invalid_roll_number_returns_400():
    r = requests.get(url("/profile"), headers={"X-Roll-Number": "abc", "X-User-ID": USER_ID})
    assert r.status_code == 400

def test_missing_user_id_on_user_scoped_endpoint_returns_400():
    r = requests.get(url("/profile"), headers={"X-Roll-Number": ROLL_NUMBER})
    assert r.status_code == 400

def test_invalid_user_id_returns_400():
    r = requests.get(url("/profile"), headers={"X-Roll-Number": ROLL_NUMBER, "X-User-ID": "-5"})
    assert r.status_code == 400

def test_admin_endpoint_does_not_need_user_id():
    r = requests.get(url("/admin/users"), headers=admin_headers())
    assert r.status_code == 200


