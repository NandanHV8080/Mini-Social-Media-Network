def comment_post(users, posts, username, post_id, comment_text):
    username = username.strip()
    comment_text = comment_text.strip()

    if username not in users:
        return False, "Only an existing user can comment on a post."

    if not comment_text:
        return False, "Comment cannot be empty."

    for post in posts:
        if post["id"] == post_id:
            post.setdefault("comments", [])

            new_comment = {
                "author": username,
                "text": comment_text
            }

            post["comments"].append(new_comment)
            return True, f"Comment added successfully to post {post_id}."

    return False, f"Post {post_id} does not exist."
