from crew_management import get_role
from inventory import car_exists

races = []

def create_race(race_name, driver_name, car_name):
    if get_role(driver_name) != 'Driver':
        return f"{driver_name} isn't a driver. Only drivers can race"
    
    if not car_exists(car_name):
        return f"{car_name} doesn't exist in inventory. Please choose a valid car."
    
    for race in races:
        if races["name"] == race_name:
            return "Race already exists"
        
    race = {
        "name": race_name,
        "driver": driver_name,
        "car": car_name,
        "status": "upcoming"    #Possible statuses are upcoming, ongoing, completed
    }
    races.append(race)
    return f"Race:{race_name} has been created"

def get_race(race_name):
    for race in races:
        if races["name"] == race_name:
            return race
    return None

def start_race(race_name):
    race = get_race(race_name)
    if not race:
        return "Race doesn't exist"
    if race["status"] != "upcoming":
        return "Race has already started or finished"
    race["status"] = "ongoing"
    return f"Race:{race_name} has been started"

def get_all_races():
    return races

def race_exits(race_name):
    return get_race(race_name) is not None