def remove_friend(users, username, friend_username):
    username = username.strip()
    friend_username = friend_username.strip()
 
    if username not in users:
        return False, f"User '{username}' does not exist."
 
    if friend_username not in users:
        return False, f"User '{friend_username}' does not exist."
 
    if username == friend_username:
        return False, "You cannot remove yourself."
 
    users[username].setdefault("friends", [])
    users[friend_username].setdefault("friends", [])
 
    if friend_username not in users[username]["friends"]:
        return False, f"{friend_username} is not in your friends list."
 
    users[username]["friends"].remove(friend_username)
 
    if username in users[friend_username]["friends"]:
        users[friend_username]["friends"].remove(username)
 
    return True, f"You are no longer friends with {friend_username}."