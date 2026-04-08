import json
import os


def save_data(users, posts, file_path="data/data.json"):
    folder = os.path.dirname(file_path)
    if folder:
        os.makedirs(folder, exist_ok=True)

    data = {
        "users": users,
        "posts": posts
    }

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

    return True, f"Data saved to {file_path}"


def load_data(file_path="data/data.json"):
    if not os.path.exists(file_path):
        return {}, []

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
    except json.JSONDecodeError:
        return {}, []

    users = data.get("users", {})
    posts = data.get("posts", [])

    return users, posts
