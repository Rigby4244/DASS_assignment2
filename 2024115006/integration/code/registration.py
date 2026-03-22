members = {}

def registration(name, role):
    if name in members:
        return "Member is existing"
    members[name] = {"role": role.lower(), "skill": 0} #default skill is 0
    return f"{name} registerted as {role}"

def get_member(name):
    return members.get(name, None)

def get_all_members():
    return members

def member_exists(name):
    return name in members
