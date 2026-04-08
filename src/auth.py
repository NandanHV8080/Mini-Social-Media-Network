def create_user(users, username, password):
    username = username.strip()

    if not username:
        return False, "Username cannot be empty."

    if not password:
        return False, "Password cannot be empty."

    if username in users:
        return False, "User already exists."

    users[username] = {
        "password": password,
        "friends": [],
        "posts": []
    }

    return True, f"Account created for {username}."


def login_user(users, username, password):
    username = username.strip()

    if username not in users:
        return False, "User does not exist."

    if users[username]["password"] != password:
        return False, "Incorrect password."

    return True, f"{username} logged in successfully."


def logout_user(current_user):
    if current_user is None:
        return None, "No user is currently logged in."

    old_user = current_user
    current_user = None
    return current_user, f"{old_user} logged out successfully."