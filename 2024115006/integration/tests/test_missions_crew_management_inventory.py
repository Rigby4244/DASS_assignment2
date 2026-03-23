from registration import registration, members
from inventory import get_cash, inventory
from missions import assign_mission, missions

import pytest

@pytest.fixture(autouse=True)
def reset():
    inventory["cash"] = 1000
    inventory["cars"] = []
    inventory["parts"] = []
    inventory["tools"] = []
    members.clear()
    missions.clear()

def test_assign_mission_with_valid_inputs():
    registration("Ahemad", "driver")
    result = assign_mission("Bombthem", "driver", 67)
    assert "Mission:Bombthem has been assigned to Ahemad" in result

def test_assign_mission_with_insufficient_cash():
    registration("Ahemad", "driver")
    result = assign_mission("Bombthem", "driver", 1500)
    assert result == "Mission failed: Not enough cash"

def test_assign_mission_with_no_available_role():
    result = assign_mission("Bombthem", "mechanic", 67)
    assert result == "Mission failed: No mechanic available"

def test_assign_mission_with_the_first_available_member():
    registration("Ahemad", "driver")
    registration("John", "driver")
    result = assign_mission("Bombthem", "driver", 67)
    assert "Mission:Bombthem has been assigned to Ahemad" in result

def test_mission_cost_deduction():
    registration("Ahemad", "driver")
    assign_mission("Bombthem", "driver", 67)
    result = get_cash()
    assert result == 933

