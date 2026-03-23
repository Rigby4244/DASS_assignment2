from finance import log_expense, get_summary, expenses
from inventory import inventory

import pytest

@pytest.fixture(autouse=True)
def reset():
    inventory["cash"] = 1000
    inventory["cars"] = []
    inventory["parts"] = []
    inventory["tools"] = []
    expenses.clear()

def test_log_expense_with_valid_input():
    result = log_expense("Car Repair", 200)
    assert "Expense logged:Car Repair, costed:200" in result

def test_log_expense_with_negative_amount():
    result = log_expense("Car Repair", -200)
    assert "Amount can't be negative" in result

def test_log_expense_with_insufficient_cash():
    result = log_expense("Car Repair", 1200)
    assert "Expense failed: Not enough cash" in result

def test_get_summary():
    log_expense("Car Repair", 200)
    log_expense("Part Purchase", 100)
    result = get_summary()
    assert {"cash_remaining": 700, "total_spent": 300, "expense_count": 2, "expenses": expenses} == result