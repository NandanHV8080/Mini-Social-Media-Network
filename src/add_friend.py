def add_friend(users, username, friend_username):
    username = username.strip()
    friend_username = friend_username.strip()

    if username not in users:
        return False, f"User '{username}' does not exist."

    if friend_username not in users:
        return False, f"User '{friend_username}' does not exist."

    if username == friend_username:
        return False, "You cannot add yourself as a friend."

    users[username].setdefault("friends", [])
    users[friend_username].setdefault("friends", [])

    if friend_username in users[username]["friends"]:
        return False, f"{friend_username} is already a friend."

    users[username]["friends"].append(friend_username)
    users[friend_username]["friends"].append(username)

    return True, f"{friend_username} added as a friend successfully."