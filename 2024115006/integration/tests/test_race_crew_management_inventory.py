from race import create_race, races
from registration import registration, members
from inventory import add_car, remove_car, inventory

import pytest

@pytest.fixture(autouse=True)
def reset():
    inventory["cash"] = 1000
    inventory["cars"] = []      # reset to empty list, don't clear the whole dict
    inventory["parts"] = []
    inventory["tools"] = []
    members.clear()             # members is a flat dict so .clear() is fine here
    races.clear()

def test_creating_a_race_with_valid_inputs():
    registration("Ahemad", "driver")
    add_car("Ferari")
    result = create_race("racetoglory", "Ahemad", "Ferari")
    assert "Race:racetoglory has been created" in result

def test_creating_a_race_without_a_car():
    registration("Ahemad", "driver")
    result = create_race("racetoglory", "Ahemad", "Ferari")
    assert "Ferari doesn't exist in inventory. Please choose a valid car." in result

def test_creating_a_race_without_a_driver():
    registration("Hamza", "mechanic")
    add_car("Ferari")
    result = create_race("racetoglory", "Ahemad", "Ferari")
    assert "Ahemad isn't a driver. Only drivers can race" in result

def test_creating_a_race_without_a_driver_and_a_car():
    add_car("Ferari")
    remove_car("Ferari")
    result = create_race("racetoglory", "Ahemad", "Ferari")
    assert "Ahemad isn't a driver. Only drivers can race" in result

def test_creating_a_race_that_already_exists():
    registration("Ahemad", "driver")
    registration("Hamza", "driver")
    add_car("Ferari")
    add_car("Lamborghini")
    create_race("racetoglory", "Ahemad", "Ferari")
    result = create_race("racetoglory", "Hamza", "Lamborghini")
    assert "Race already exists" in result