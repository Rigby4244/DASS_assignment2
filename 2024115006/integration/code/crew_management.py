from registration import get_member, get_all_members, member_exits

def update_skill(name, skill_level):
    if not member_exits(name):
        return "Member isn't registered"
    if skill_level < 0 or skill_level > 100:
        return "Skill level must be between 0 and 100(inclusive)"
    member = get_member(name)
    member["skill"] = skill_level
    return "{name}'s skill level is now {skill_level}"

def get_role(name):
    if not member_exits(name):
        return "Member isn't registered"
    member = get_member(name)
    return member["role"]

def get_skill_level(name):
    if not member_exits(name):
        return "Member isn't registered"
    member = get_member(name)
    return member["skill"]

def get_members_by_role(role):
    all_members = get_all_members()
    return [name for name, data in all_members.items() if data["role"] == role]