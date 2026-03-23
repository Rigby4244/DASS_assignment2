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

def test_list_products_returns_200():
    r = requests.get(url("/products"), headers=headers())
    assert r.status_code == 200

def test_inactive_products_not_in_list():
    r_active = requests.get(url("/products"), headers=headers()).json()
    r_admin = requests.get(url("/admin/products"), headers=admin_headers()).json()
    active_list = r_active.get("products") if isinstance(r_active, dict) else r_active
    admin_list = r_admin.get("products") if isinstance(r_admin, dict) else r_admin
    active_ids = {p["product_id"] for p in active_list}
    inactive = [p for p in admin_list if not p.get("is_active")]
    for p in inactive:
        assert p["product_id"] not in active_ids, f"Inactive product {p['product_id']} appeared in public list!"

def test_get_product_by_id_returns_200():
    h = headers()
    r_products = requests.get(url("/products"), headers=h).json()
    products = r_products.get("products") if isinstance(r_products, dict) else r_products
    if not products:
        pytest.skip("No products available to fetch by ID")
    pid = products[0]["product_id"]
    r = requests.get(url(f"/products/{pid}"), headers=h)
    assert r.status_code == 200

def test_get_nonexistent_product_returns_404():
    r = requests.get(url("/products/999999"), headers=headers())
    assert r.status_code == 404

def test_product_price_matches_admin():
    h = headers()
    adm_h = admin_headers()
    r_public = requests.get(url("/products"), headers=h).json()
    products = r_public.get("products") if isinstance(r_public, dict) else r_public
    if not products:
        pytest.skip("No products found to test")
    p = products[0]
    r_admin = requests.get(url("/admin/products"), headers=adm_h).json()
    admin_products = r_admin.get("products") if isinstance(r_admin, dict) else r_admin
    admin_p = next((x for x in admin_products if x["product_id"] == p["product_id"]), None)
    assert admin_p is not None, f"Product {p['product_id']} not found in admin list"
    assert float(p["price"]) == float(admin_p["price"])

#Instructions not given for sorting, so couldn't test that.