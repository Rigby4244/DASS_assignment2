from leaderboard import show_leaderboard, get_top_driver, get_driver_stats
from results import record_race, results, ranking
from registration import registration, members
from race import create_race, start_race, races
from inventory import add_car, get_cash, inventory

import pytest

@pytest.fixture(autouse=True)
def reset():
    inventory["cash"] = 1000
    inventory["cars"] = []
    inventory["parts"] = []
    inventory["tools"] = []
    members.clear()
    races.clear()
    results.clear()
    ranking.clear()

def test_show_leaderboard():
    registration("Ahemad", "driver")
    add_car("Ferari")
    create_race("racetoglory", "Ahemad", "Ferari")
    start_race("racetoglory")
    record_race("racetoglory", 1, 800)
    result = show_leaderboard()
    assert result == [("Ahemad", 9)]

def test_show_leaderboard_no_results():
    result = show_leaderboard()
    assert "No driver is ranked yet" in result

def test_show_leaderboard_tie():
    registration("Ahemad", "driver")
    registration("Hamza", "driver")
    add_car("Ferari")
    add_car("Lamborghini")
    create_race("racetoglory1", "Ahemad", "Ferari")
    create_race("racetoglory2", "Hamza", "Lamborghini")
    start_race("racetoglory1")
    start_race("racetoglory2")
    record_race("racetoglory1", 1, 800)
    record_race("racetoglory2", 1, 800)
    result = show_leaderboard()
    assert result == [("Ahemad", 9), ("Hamza", 9)]

def test_show_leaderboard_sorted():
    registration("Ahemad", "driver")
    registration("Hamza", "driver")
    add_car("Ferari")
    add_car("Lamborghini")
    create_race("racetoglory1", "Ahemad", "Ferari")
    create_race("racetoglory2", "Hamza", "Lamborghini")
    start_race("racetoglory1")
    start_race("racetoglory2")
    record_race("racetoglory1", 1, 800)
    record_race("racetoglory2", 2, 500)
    result = show_leaderboard()
    assert result == [("Ahemad", 9), ("Hamza", 8)]

def test_get_top_driver():
    registration("Ahemad", "driver")
    registration("Hamza", "driver")
    add_car("Ferari")
    add_car("Lamborghini")
    create_race("racetoglory1", "Ahemad", "Ferari")
    create_race("racetoglory2", "Hamza", "Lamborghini")
    start_race("racetoglory1")
    start_race("racetoglory2")
    record_race("racetoglory1", 1, 800)
    record_race("racetoglory2", 2, 500)
    result = get_top_driver()
    assert result == "Ahemad"

def test_get_top_driver_no_drivers():
    result = get_top_driver()
    assert "No drivers is ranked yet" in result

def test_get_driver_stats():
    registration("Ahemad", "driver")
    add_car("Ferari")
    create_race("racetoglory", "Ahemad", "Ferari")
    start_race("racetoglory")
    record_race("racetoglory", 1, 800)
    stats = get_driver_stats("Ahemad")
    assert stats == {"races": 1, "total_prize": 800}

def test_get_driver_stats_no_races():
    registration("Ahemad", "driver")
    stats = get_driver_stats("Ahemad")
    assert stats == {"races": 0, "total_prize": 0}

def test_get_driver_stats_multiple_races():
    registration("Ahemad", "driver")
    add_car("Ferari")
    create_race("racetoglory1", "Ahemad", "Ferari")
    create_race("racetoglory2", "Ahemad", "Ferari")
    start_race("racetoglory1")
    start_race("racetoglory2")
    record_race("racetoglory1", 1, 800)
    record_race("racetoglory2", 2, 500)
    stats = get_driver_stats("Ahemad")
    assert stats == {"races": 2, "total_prize": 1300}