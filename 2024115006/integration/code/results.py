from race import get_race
from inventory import add_cash

results = []
ranking = {}

def record_race(race_name, position, prize_money):
    race = get_race(race_name)

    if not race:
        return "Race doesn't exist"
    
    if race["status"] != "ongoing":
        return "Race isn't ongoing. Either didn't start or completed"
    
    driver_name = race["driver"]

    results.append[{
        "race": race_name,
        "driver": driver_name,
        "position": position,
        "prize": prize_money
    }]

    race["status"] = "completed"

    points = max(0, 10 - position)
    ranking[driver_name] = ranking.get(driver_name, 0) + points

    add_cash(prize_money)

    return f"Drive:{driver_name} has finished and earned prize money:{prize_money}"

def get_results():
    return results

def get_ranking():
    return ranking

def get_driver_ranking(driver_name):
    return ranking.get(driver_name, 0)