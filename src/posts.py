def create_post(users, posts, author, content):
    author = author.strip()
    content = content.strip()

    if author not in users:
        return False, "Only an existing user can create a post."

    if not content:
        return False, "Post content cannot be empty."

    next_id = 1
    if posts:
        next_id = posts[-1]["id"] + 1

    new_post = {
        "id": next_id,
        "author": author,
        "content": content,
        "likes": [],
        "comments": []
    }

    posts.append(new_post)

    users[author].setdefault("posts", [])
    users[author]["posts"].append(next_id)

    return True, f"Post {next_id} created successfully."