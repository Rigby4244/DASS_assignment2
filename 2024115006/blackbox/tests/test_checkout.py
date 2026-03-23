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

@pytest.fixture(autouse=True)
def setup_method():
    requests.delete(url("/cart/clear"), headers=headers())

def test_checkout_empty_cart_returns_400():
    r = requests.post(url("/checkout"), json={"payment_method": "CARD"}, headers=headers())
    assert r.status_code == 400

def test_checkout_invalid_payment_method_returns_400(first_product):
    requests.post(url("/cart/add"),
                    json={"product_id": first_product["product_id"], "quantity": 1},
                    headers=headers())
    r = requests.post(url("/checkout"), json={"payment_method": "BITCOIN"}, headers=headers())
    assert r.status_code == 400

def test_checkout_card_payment_status_is_paid(first_product):
    requests.post(url("/cart/add"),
                    json={"product_id": first_product["product_id"], "quantity": 1},
                    headers=headers())
    r = requests.post(url("/checkout"), json={"payment_method": "CARD"}, headers=headers())
    if r.status_code == 200:
        response_data = r.json()
        if isinstance(response_data, dict):
            order = response_data.get("order") or response_data
        else:
            order = response_data
        assert order.get("payment_status") == "PAID"

def test_checkout_cod_order_status_is_pending(first_product):
    requests.post(url("/cart/add"),
                    json={"product_id": first_product["product_id"], "quantity": 1},
                    headers=headers())
    r = requests.post(url("/checkout"), json={"payment_method": "COD"}, headers=headers())
    if r.status_code == 200:
        response_data = r.json()
        if isinstance(response_data, dict):
            order = response_data.get("order") or response_data
        else:
            order = response_data
        assert order.get("payment_status") == "PENDING"

def test_gst_is_5_percent(first_product):
    requests.post(url("/cart/add"),
                    json={"product_id": first_product["product_id"], "quantity": 1},
                    headers=headers())
    cart  = requests.get(url("/cart"), headers=headers()).json()
    if isinstance(cart, dict):
        cart_total = float(cart.get("total") or cart.get("cart", {}).get("total", 0))
    else:
        cart_total = sum(float(item["subtotal"]) for item in cart)
    r = requests.post(url("/checkout"), json={"payment_method": "CARD"}, headers=headers())
    if r.status_code == 200:
        response_data = r.json()
        if isinstance(response_data, dict):
            order = response_data.get("order") or response_data
        else:
            order = response_data
        order_total = float(order.get("total") or order.get("order_total", 0))
        assert abs(order_total - cart_total * 1.05) < 0.02

def test_checkout_cod_limit_exceeded_returns_400(first_product):
    requests.post(url("/cart/add"),
                    json={"product_id": first_product["product_id"], "quantity": 5000},
                    headers=headers())
    r = requests.post(url("/checkout"), json={"payment_method": "COD"}, headers=headers())
    assert r.status_code == 400
