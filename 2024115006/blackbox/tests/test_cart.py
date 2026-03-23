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
    r = requests.get(url("/products"), headers=headers())
    products = r.json()
    if isinstance(products, dict):
        products = products.get("products") or products
    return products[0]

@pytest.fixture(autouse=True)
def clear_cart():
    requests.delete(url("/cart/clear"), headers=headers())

def test_get_cart_returns_200():
    r = requests.get(url("/cart"), headers=headers())
    assert r.status_code == 200

def test_add_item_valid(first_product):
    r = requests.post(url("/cart/add"),
                        json={"product_id": first_product["product_id"], "quantity": 1},
                        headers=headers())
    assert r.status_code in (200, 201)

def test_add_item_zero_quantity_returns_400(first_product):
    r = requests.post(url("/cart/add"),
                        json={"product_id": first_product["product_id"], "quantity": 0},
                        headers=headers())
    assert r.status_code == 400

def test_add_item_negative_quantity_returns_400(first_product):
    r = requests.post(url("/cart/add"),
                        json={"product_id": first_product["product_id"], "quantity": -1},
                        headers=headers())
    assert r.status_code == 400

def test_add_nonexistent_product_returns_404():
    r = requests.post(url("/cart/add"),
                        json={"product_id": 999999, "quantity": 1},
                        headers=headers())
    assert r.status_code == 404

def test_add_same_product_twice_accumulates_quantity(first_product):
    pid = first_product["product_id"]
    requests.post(url("/cart/add"), json={"product_id": pid, "quantity": 1}, headers=headers())
    requests.post(url("/cart/add"), json={"product_id": pid, "quantity": 2}, headers=headers())
    cart = requests.get(url("/cart"), headers=headers()).json()
    if isinstance(cart, dict):
        items = cart.get("items") or cart.get("cart", {}).get("items", [])
    else:
        items = cart
    item  = next((i for i in items if i["product_id"] == pid), None)
    assert item is not None
    assert item["quantity"] == 3

def test_cart_subtotal_is_quantity_times_price(first_product):
    pid   = first_product["product_id"]
    price = float(first_product["price"])
    requests.post(url("/cart/add"), json={"product_id": pid, "quantity": 3}, headers=headers())
    cart  = requests.get(url("/cart"), headers=headers()).json()
    if isinstance(cart, dict):
        items = cart.get("items") or cart.get("cart", {}).get("items", [])
    else:
        items = cart
    item  = next((i for i in items if i["product_id"] == pid), None)
    assert abs(float(item["subtotal"]) - price * 3) < 0.01

def test_cart_total_equals_sum_of_subtotals(first_product):
    requests.post(url("/cart/add"),
                    json={"product_id": first_product["product_id"], "quantity": 2},
                    headers=headers())
    cart   = requests.get(url("/cart"), headers=headers()).json()
    if isinstance(cart, dict):
        items  = cart.get("items") or cart.get("cart", {}).get("items", [])
        total  = float(cart.get("total") or cart.get("cart", {}).get("total", 0))
    else:
        items = cart
        total = sum(float(i["subtotal"]) for i in items)
    expected = sum(float(i["subtotal"]) for i in items)
    assert abs(total - expected) < 0.01

def test_remove_item_not_in_cart_returns_404(first_product):
    r = requests.post(url("/cart/remove"),
                        json={"product_id": first_product["product_id"]},
                        headers=headers())
    assert r.status_code == 404

def test_update_item_zero_quantity_returns_400(first_product):
    pid = first_product["product_id"]
    requests.post(url("/cart/add"), json={"product_id": pid, "quantity": 1}, headers=headers())
    r = requests.post(url("/cart/update"), json={"product_id": pid, "quantity": 0}, headers=headers())
    assert r.status_code == 400

def test_add_more_than_stock_returns_400(first_product):
    r = requests.post(url("/cart/add"),
                        json={"product_id": first_product["product_id"], "quantity": 999999},
                        headers=headers())
    assert r.status_code == 400