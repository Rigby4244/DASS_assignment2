inventory = {
    "cash": 1000, #default cash: 1000
    "cars": [],
    "parts": [],
    "tools": []
}

def add_cash(amount):
    if amount < 0:
        return "Amount can't be negative"
    inventory["cash"] += amount
    return inventory["cash"]

def deduct_cash(amount):
    if amount < 0:
        return "Amount can't be negative"
    if amount > inventory["cash"]:
        return "Amount can't be greater than existing cash"
    inventory["cash"] -= amount
    return inventory["cash"]

def get_cash():
    return inventory["cash"]

#----------------------------------------------------------------------

def add_car(name):
    if name in inventory["cars"]:
        return "Car already exists"
    inventory["cars"].append(name)
    return f"Car:{name} has been added"

def remove_car(name):
    if name not in inventory["cars"]:
        return "Car doesn't exist"
    inventory["cars"].remove(name)
    return f"Car:{name} has been removed"

def get_cars():
    return inventory["cars"]

def car_exists(name):
    return name in inventory["cars"]

#----------------------------------------------------------------------

def add_part(name):
    if name in inventory["parts"]:
        return "Part already exists"
    inventory["parts"].append(name)
    return f"Part:{name} has been added"

def remove_part(name):
    if name not in inventory["parts"]:
        return "Part doesn't exist"
    inventory["parts"].remove(name)
    return f"Part:{name} has been removed"

def get_parts():
    return inventory["parts"]

def part_exists(name):
    return name in inventory["parts"]