from registration import registration, members
from race import create_race, start_race, races
from results import record_race
from inventory import add_car, remove_car, inventory

import pytest

@pytest.fixture(autouse=True)
def reset():
    inventory["cash"] = 1000
    inventory["cars"] = []
    inventory["parts"] = []
    inventory["tools"] = []
    members.clear()
    races.clear()

def test_record_race_results_with_valid_inputs():
    registration("Ahemad", "driver")
    add_car("Ferari")
    create_race("racetoglory", "Ahemad", "Ferari")
    start_race("racetoglory")
    result = record_race("racetoglory", 1, 800)
    assert "Drive:Ahemad has finished and earned prize money:800" in result

def test_record_race_with_nonexistent_race():
    result = record_race("racetoglory", 1, 800)
    assert "Race doesn't exist" in result

def test_record_race_with_non_ongoing_race():
    registration("Ahemad", "driver")
    add_car("Ferari")
    create_race("racetoglory", "Ahemad", "Ferari")
    result = record_race("racetoglory", 1, 800)
    assert "Race isn't ongoing. Either didn't start or completed" in result

def test_record_race_with_invalid_position():
    registration("Ahemad", "driver")
    add_car("Ferari")
    create_race("racetoglory", "Ahemad", "Ferari")
    start_race("racetoglory")
    result = record_race("racetoglory", -1, 800)
    assert "Invalid position, position must be a positive integer" in result

def test_record_race_with_invalid_prize_money():
    registration("Ahemad", "driver")
    add_car("Ferari")
    create_race("racetoglory", "Ahemad", "Ferari")
    start_race("racetoglory")
    result = record_race("racetoglory", 1, -100)
    assert "Invalid prize money, prize money must be a non-negative integer" in result