def delete_post(users, posts, author, post_id):
    author = author.strip()

    if author not in users:
        return False, "Only an existing user can delete a post."

    for index, post in enumerate(posts):
        if post["id"] == post_id:
            if post["author"] != author:
                return False, "You can only delete your own posts."

            del posts[index]

            users[author].setdefault("posts", [])
            if post_id in users[author]["posts"]:
                users[author]["posts"].remove(post_id)

            return True, f"Post {post_id} deleted successfully."

    return False, f"Post {post_id} does not exist."
