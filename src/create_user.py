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

