from inventory import deduct_cash, get_cash

expenses = []

def log_expense(description, amount):
    if amount < 0:
        return "Amount can't be negative"
    
    result = deduct_cash(amount)
    if result == "Amount can't be greater than existing cash":
        return "Expense failed: Not enough cash"

    expenses.append({
        "description": description,
        "amount": amount
    })
    return f"Expense logged:{description}, costed:{amount}"

def get_total_spent():
    return sum(e["amount"] for e in expenses)

def get_summary():
    return {
        "cash_remaining": get_cash(),
        "total_spent": get_total_spent(),
        "expense_count": len(expenses),
        "expenses": expenses
    }

def get_all_expenses():
    return expenses