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

@pytest.fixture(scope="module")
def first_product():
    """Returns first active product for cart tests."""
    r = requests.get(url("/products"), headers=headers())
    products = r.json()
    if isinstance(products, dict):
        products = products.get("products") or products
    return products[0]

def test_get_orders_returns_200():
    r = requests.get(url("/orders"), headers=headers())
    assert r.status_code == 200

def test_cancel_nonexistent_order_returns_404():
    r = requests.post(url("/orders/999999/cancel"), headers=headers())
    assert r.status_code == 404

def test_invoice_structure():
    orders = requests.get(url("/orders"), headers=headers()).json()
    if isinstance(orders, dict):
        order_list = orders.get("orders") or orders
    else:
        order_list = orders
    if not order_list:
        pytest.skip("No orders to test invoice on")
    oid = order_list[0]["order_id"]
    r = requests.get(url(f"/orders/{oid}/invoice"), headers=headers())
    assert r.status_code == 200
    body = r.json()
    for field in ("subtotal", "gst_amount", "total_amount"):
        if isinstance(body, dict):
            assert field in body or field in body.get("invoice", {})
        else:
            assert any(field in item for item in body if isinstance(item, dict))

def test_cancelled_items_are_restocked(first_product):
    requests.post(url("/cart/add"), json={"product_id": first_product["product_id"], "quantity": 1}, headers=headers())
    r = requests.post(url("/checkout"), json={"payment_method": "CARD"}, headers=headers())
    assert r.status_code == 200
    order = r.json().get("order") or r.json()
    oid = order["order_id"]
    r = requests.post(url(f"/orders/{oid}/cancel"), headers=headers())
    assert r.status_code == 200
    r = requests.get(url("/products"), headers=headers())
    products = r.json()
    if isinstance(products, dict):
        products = products.get("products") or products
    for p in products:
        if p["product_id"] == first_product["product_id"]:
            stock_field = p.get("stock") or p.get("stock_quantity") or p.get("quantity")
            assert stock_field is not None
            assert stock_field >= 1
            break
    else:
        pytest.fail()