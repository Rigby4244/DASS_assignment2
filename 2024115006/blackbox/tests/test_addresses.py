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

def test_get_addresses_returns_200():
    r = requests.get(url("/addresses"), headers=headers())
    assert r.status_code == 200

def test_add_address_valid():
    payload = {
        "label": "OFFICE",
        "street": "456 Office Road",
        "city": "Bangalore",
        "pincode": "560001",
        "is_default": False
    }
    r = requests.post(url("/addresses"), json=payload, headers=headers())
    assert r.status_code in (200, 201)
    body = r.json()
    addr = body.get("address") or body #sucessful post must also return address_id
    assert "address_id" in addr

def test_add_address_invalid_label_returns_400():
    payload = {"label": "SCHOOL", "street": "123 Road", "city": "Delhi", "pincode": "110001"}
    r = requests.post(url("/addresses"), json=payload, headers=headers())
    assert r.status_code == 400

def test_add_address_short_street_returns_400():
    payload = {"label": "HOME", "street": "Hi", "city": "Delhi", "pincode": "110001"}
    r = requests.post(url("/addresses"), json=payload, headers=headers())
    assert r.status_code == 400

def test_add_address_invalid_pincode_returns_400():
    payload = {"label": "HOME", "street": "123 Long Street", "city": "Delhi", "pincode": "1234"}
    r = requests.post(url("/addresses"), json=payload, headers=headers())
    assert r.status_code == 400

def test_add_address_invalid_city_returns_400():
    payload = {"label": "HOME", "street": "123 Long Street", "city": "X", "pincode": "110001"}
    r = requests.post(url("/addresses"), json=payload, headers=headers())
    assert r.status_code == 400

def test_only_one_default_address():
    h = headers()
    p1 = {"label": "HOME", "street": "First Street 1", "city": "Chennai", "pincode": "600001", "is_default": True}
    p2 = {"label": "OTHER", "street": "Second Street 2", "city": "Chennai", "pincode": "600002", "is_default": True}
    id1 = None
    id2 = None
    try:
        r1 = requests.post(url("/addresses"), json=p1, headers=h)
        assert r1.status_code in [200, 201], f"Failed to create p1: {r1.text}"
        id1 = (r1.json().get("address") or r1.json()).get("address_id")
        r2 = requests.post(url("/addresses"), json=p2, headers=h)
        assert r2.status_code in [200, 201], f"Failed to create p2: {r2.text}"
        id2 = (r2.json().get("address") or r2.json()).get("address_id")
        response = requests.get(url("/addresses"), headers=h)
        all_addr = response.json()
        address_list = all_addr.get("addresses") if isinstance(all_addr, dict) else all_addr
        defaults = [a for a in address_list if isinstance(a, dict) and a.get("is_default") is True]
        assert len(defaults) == 1
        assert defaults[0].get("address_id") == id2
    finally:
        for aid in [id1, id2]:
            if aid:
                requests.delete(url(f"/addresses/{aid}"), headers=h)

def test_delete_nonexistent_address_returns_404():
    r = requests.delete(url("/addresses/999999"), headers=headers())
    assert r.status_code == 404


def test_update_address_response_shows_new_data():
    h = headers()
    payload = {"label": "HOME", "street": "123 Test Street", "city": "Hyderabad", "pincode": "500001", "is_default": False}
    post_r = requests.post(url("/addresses"), json=payload, headers=h)
    assert post_r.status_code == 201 or post_r.status_code == 200
    data = post_r.json()
    address_id = data.get("address_id") or data.get("address", {}).get("address_id")    
    assert address_id is not None
    try:
        new_street = "Updated Street 99"
        update_r = requests.put(url(f"/addresses/{address_id}"), json={"street": new_street, "is_default": False}, headers=h)
        if update_r.status_code != 200:
            print(f"DEBUG: PUT failed for ID {address_id}. Response: {update_r.text}")
        assert update_r.status_code == 200
        body = update_r.json()
        addr = body.get("address") or body
        assert addr.get("street") == new_street
    finally:
        if address_id:
            requests.delete(url(f"/addresses/{address_id}"), headers=h)

def test_update_restricted_fields_returns_400():
    h = headers()
    payload = {"label": "HOME", "street": "123 Test Street", "city": "Hyderabad", "pincode": "500001", "is_default": False}
    post_r = requests.post(url("/addresses"), json=payload, headers=h)
    assert post_r.status_code in (200, 201)
    data = post_r.json()
    address_id = data.get("address_id") or data.get("address", {}).get("address_id")
    assert address_id is not None
    try:
        update_r = requests.put(url(f"/addresses/{address_id}"), json={"label": "OFFICE", "city": "Chennai", "pincode": "600001"}, headers=h)
        assert update_r.status_code == 400
    finally:
        if address_id:
            requests.delete(url(f"/addresses/{address_id}"), headers=h)

def test_add_address_with_invalid_pincode_format_returns_400():
    payload = {"label": "HOME", "street": "123 Long Street", "city": "Delhi", "pincode": "ABCDEF"}
    r = requests.post(url("/addresses"), json=payload, headers=headers())
    assert r.status_code == 400