from registration import registration, members
from crew_management import update_skill, get_role, get_skill_level, get_members_by_role

import pytest

@pytest.fixture(autouse=True)
def reset():
    members.clear()

def test_assign_skill_to_registered_member():
    registration("Mohamad", "Driver")
    result = update_skill("Mohamad", 80)
    assert "Mohamad's skill level is now 80" in result

def test_assign_skill_to_unregistered_member():
    result = update_skill("Hamza", 80)
    assert "Member isn't registered" in result

def test_skill_out_of_range():
    registration("Mohamad", "Driver")
    result = update_skill("Mohamad", 150)
    assert "Skill level must be between 0 and 100(inclusive)" in result

def test_get_role_of_registered_member():
    registration("Mohamad", "Driver")
    result = get_role("Mohamad")
    assert "driver" == result

def test_get_role_of_unregistered_member():
    result = get_role("Hamza")
    assert None is result

def test_get_skill_level_of_registered_member():
    registration("Mohamad", "Driver")
    update_skill("Mohamad", 80)
    result = get_skill_level("Mohamad")
    assert 80 == result

def test_get_skill_level_of_unregistered_member():
    result = get_skill_level("Hamza")
    assert "Member isn't registered" in result

def test_get_members_by_role():
    registration("Mohamad", "Driver")
    registration("Sara", "Driver")
    registration("Hamza", "Mechanic")
    result = get_members_by_role("driver")
    assert ["Mohamad", "Sara"] == result

def test_get_members_by_role_with_no_members():
    registration("Hamza", "Mechanic")
    result = get_members_by_role("driver")
    assert [] == result