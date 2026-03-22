from crew_management import get_members_by_role
from inventory import get_cash, deduct_cash

missions = []

def assign_mission(mission_name, required_role, cost):
    available = get_members_by_role(required_role)
    
    if not available:
        return f"Mission failed: No {required_role} available"
    
    if get_cash() < cost:
        return "Mission failed: Not enough cash"
    
    deduct_cash(cost)

    mission = {
        "name": mission_name,
        "role_needed": required_role,
        "assigned_to": available[0],  # assigning to the first available member
        "cost": cost,
        "status": "active"
    }
    missions.append(mission)
    return f"Mission:{mission_name} has been assigned to {available[0]}"

def complete_mission(mission_name):
    mission = get_mission(mission_name)
    if not mission:
        return "Mission doesn't exist"
    mission["status"] = "completed"
    return f"Mission:{mission_name} has been completed"

def get_mission(mission_name):
    for mission in missions:
        if mission["name"] == mission_name:
            return mission
    return None

def get_all_missions():
    return missions