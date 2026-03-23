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

def test_create_valid_ticket():
    r = requests.post(url("/support/ticket"), json={"subject": "Test subject here", "message": "Detailed message for the ticket."}, headers=headers())
    assert r.status_code in (200, 201)

def test_create_ticket_subject_too_short_returns_400():
    r = requests.post(url("/support/ticket"), json={"subject": "Hi", "message": "Valid message here"}, headers=headers())
    assert r.status_code == 400

def test_create_ticket_subject_too_long_returns_400():
    r = requests.post(url("/support/ticket"), json={"subject": "A" * 101, "message": "Valid message here"}, headers=headers())
    assert r.status_code == 400

def test_create_ticket_empty_message_returns_400():
    r = requests.post(url("/support/ticket"), json={"subject": "Valid subject", "message": ""}, headers=headers())
    assert r.status_code == 400

def test_create_ticket_message_over_500_returns_400():
    r = requests.post(url("/support/ticket"), json={"subject": "Valid subject", "message": "B" * 501}, headers=headers())
    assert r.status_code == 400

def test_new_ticket_status_is_open():
    r = requests.post(url("/support/ticket"), json={"subject": "Status check ticket", "message": "Is status OPEN?"}, headers=headers())
    body = r.json()
    ticket = body.get("ticket") or body
    assert ticket.get("status") == "OPEN"

def test_get_tickets_returns_200():
    r = requests.get(url("/support/tickets"), headers=headers())
    assert r.status_code == 200

def test_invalid_status_transition_returns_400():
    r = requests.post(url("/support/ticket"), json={"subject": "Transition test", "message": "Testing transition"}, headers=headers())
    ticket_id = (r.json().get("ticket") or r.json()).get("ticket_id")
    if ticket_id:
        r2 = requests.put(url(f"/support/tickets/{ticket_id}"), json={"status": "CLOSED"}, headers=headers())
        assert r2.status_code == 400

def test_valid_status_transition_open_to_in_progress():
    r = requests.post(url("/support/ticket"), json={"subject": "Progress test ticket", "message": "Moving to in progress"}, headers=headers())
    ticket_id = (r.json().get("ticket") or r.json()).get("ticket_id")
    if ticket_id:
        r2 = requests.put(url(f"/support/tickets/{ticket_id}"), json={"status": "IN_PROGRESS"}, headers=headers())
        assert r2.status_code == 200
