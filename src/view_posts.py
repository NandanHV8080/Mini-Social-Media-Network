def view_all_posts(posts):
    if not posts:
        return False, "No posts available."

    visible_posts = []

    for post in posts:
        likes_count = len(post.get("likes", []))
        comments_count = len(post.get("comments", []))

        formatted_post = (
            f"Post ID: {post['id']}\n"
            f"Author: {post['author']}\n"
            f"Content: {post['content']}\n"
            f"Likes: {likes_count}\n"
            f"Comments: {comments_count}"
        )

        visible_posts.append(formatted_post)

    return True, visible_posts
