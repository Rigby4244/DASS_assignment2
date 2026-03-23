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

@pytest.fixture
def product_id():
    products = requests.get(url("/products"), headers=headers()).json()
    if isinstance(products, dict):
        products = products.get("products") or products
    return products[0]["product_id"]

def test_get_reviews_returns_200(product_id):
    r = requests.get(url(f"/products/{product_id}/reviews"), headers=headers())
    assert r.status_code == 200

def test_add_valid_review(product_id):
    r = requests.post(url(f"/products/{product_id}/reviews"), json={"rating": 4, "comment": "Good product!"}, headers=headers())
    assert r.status_code in (200, 201)

def test_rating_zero_returns_400(product_id):
    r = requests.post(url(f"/products/{product_id}/reviews"), json={"rating": 0, "comment": "Bad"}, headers=headers())
    assert r.status_code == 400

def test_rating_six_returns_400(product_id):
    r = requests.post(url(f"/products/{product_id}/reviews"), json={"rating": 6, "comment": "Too high"}, headers=headers())
    assert r.status_code == 400

def test_rating_boundary_1_valid(product_id):
    r = requests.post(url(f"/products/{product_id}/reviews"), json={"rating": 1, "comment": "Minimum rating"}, headers=headers())
    assert r.status_code in (200, 201)

def test_rating_boundary_5_valid(product_id):
    r = requests.post(url(f"/products/{product_id}/reviews"), json={"rating": 5, "comment": "Maximum rating"}, headers=headers())
    assert r.status_code in (200, 201)

def test_empty_comment_returns_400(product_id):
    r = requests.post(url(f"/products/{product_id}/reviews"), json={"rating": 3, "comment": ""}, headers=headers())
    assert r.status_code == 400

def test_comment_over_200_chars_returns_400(product_id):
    r = requests.post(url(f"/products/{product_id}/reviews"), json={"rating": 3, "comment": "A" * 201}, headers=headers())
    assert r.status_code == 400

def test_average_rating_is_decimal_not_integer(product_id):
    requests.post(url(f"/products/{product_id}/reviews"), json={"rating": 1, "comment": "Low"}, headers=headers())
    requests.post(url(f"/products/{product_id}/reviews"), json={"rating": 2, "comment": "Higher"}, headers=headers())
    r = requests.get(url(f"/products/{product_id}/reviews"), headers=headers())
    body = r.json()
    if isinstance(body, dict):
        avg = body.get("average_rating")
    else:
        avg = None
    if avg is not None:
        assert isinstance(avg, float)

