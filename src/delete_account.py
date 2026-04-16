def delete_account(users, username, current_user=None, posts=None):
    username = username.strip()

    if not username:
        return False, "Username cannot be empty.", current_user

    if username not in users:
        return False, "User does not exist.", current_user

    # Remove this user from other users' friends lists
    for other_user in users:
        users[other_user].setdefault("friends", [])
        if username in users[other_user]["friends"]:
            users[other_user]["friends"].remove(username)

    # Remove this user's posts as well, if posts list is provided
    if posts is not None:
        remaining_posts = []
        deleted_post_ids = set()

        for post in posts:
            if post.get("author") == username:
                deleted_post_ids.add(post.get("id"))
            else:
                remaining_posts.append(post)

        posts[:] = remaining_posts

        # Also remove deleted post ids from every user's posts list
        for other_user in users:
            users[other_user].setdefault("posts", [])
            users[other_user]["posts"] = [
                post_id for post_id in users[other_user]["posts"]
                if post_id not in deleted_post_ids
            ]

    # If the deleted user is currently logged in, log them out
    if current_user == username:
        current_user = None

    del users[username]

    return True, f"Account {username} deleted successfully.", current_user

