def like_post(users, posts, username, post_id):
    username = username.strip()

    if username not in users:
        return False, "Only an existing user can like a post."

    for post in posts:
        if post["id"] == post_id:
            post.setdefault("likes", [])

            if username in post["likes"]:
                return False, f"User {username} has already liked post {post_id}."

            post["likes"].append(username)
            return True, f"Post {post_id} liked successfully."

    return False, f"Post {post_id} does not exist."
