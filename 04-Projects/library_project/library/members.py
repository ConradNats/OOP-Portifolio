# library/members.py

members = []


def register_member(name):
    members.append(name)
    return f"{name} registered successfully."


def search_member(name):
    if name in members:
        return f"{name} is a registered member."
    return f"{name} is not registered."
