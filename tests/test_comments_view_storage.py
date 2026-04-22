import json
import os
import sys
import tempfile
import unittest

# Allow imports from src/
sys.path.append(os.path.abspath("src"))

from storage import save_data, load_data
from comment_post import comment_post
from view_posts import view_all_posts


class TestCommentsViewStorage(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_file = os.path.join(self.temp_dir.name, "test_data.json")

        self.users = {
            "alice": {"password": "123", "friends": [], "posts": [1]},
            "bob": {"password": "456", "friends": [], "posts": []}
        }

        self.posts = [
            {
                "id": 1,
                "author": "alice",
                "content": "Hello world",
                "likes": ["bob"],
                "comments": []
            }
        ]

    def tearDown(self):
        self.temp_dir.cleanup()

    # -----------------------------
    # Tests for save_data / load_data
    # -----------------------------

    def test_save_data_success(self):
        result = save_data(self.users, self.posts, self.test_file)
        self.assertEqual(result, (True, f"Data saved to {self.test_file}"))
        self.assertTrue(os.path.exists(self.test_file))

    def test_load_data_success(self):
        save_data(self.users, self.posts, self.test_file)
        loaded_users, loaded_posts = load_data(self.test_file)
        self.assertEqual(loaded_users, self.users)
        self.assertEqual(loaded_posts, self.posts)

    def test_load_data_missing_file_returns_empty_structures(self):
        missing_file = os.path.join(self.temp_dir.name, "missing.json")
        self.assertEqual(load_data(missing_file), ({}, []))

    def test_load_data_invalid_json_returns_empty_structures(self):
        with open(self.test_file, "w", encoding="utf-8") as file:
            file.write('{"users":')
        self.assertEqual(load_data(self.test_file), ({}, []))

    def test_load_data_missing_posts_key_uses_default(self):
        data = {"users": {"alice": {"password": "123"}}}
        with open(self.test_file, "w", encoding="utf-8") as file:
            json.dump(data, file)

        loaded_users, loaded_posts = load_data(self.test_file)
        self.assertEqual(loaded_users, data["users"])
        self.assertEqual(loaded_posts, [])

    def test_load_data_missing_users_key_uses_default(self):
        data = {"posts": [{"id": 1, "author": "alice", "content": "Hello"}]}
        with open(self.test_file, "w", encoding="utf-8") as file:
            json.dump(data, file)

        loaded_users, loaded_posts = load_data(self.test_file)
        self.assertEqual(loaded_users, {})
        self.assertEqual(loaded_posts, data["posts"])

    def test_save_data_non_serializable_input_raises_type_error(self):
        bad_users = {"alice": {"password": set([1, 2])}}
        with self.assertRaises(TypeError):
            save_data(bad_users, self.posts, self.test_file)

    # -----------------------------
    # Tests for comment_post
    # -----------------------------

    def test_comment_post_success(self):
        result = comment_post(self.users, self.posts, "bob", 1, "Nice post!")
        self.assertEqual(result, (True, "Comment added successfully to post 1."))
        self.assertEqual(len(self.posts[0]["comments"]), 1)
        self.assertEqual(self.posts[0]["comments"][0]["author"], "bob")
        self.assertEqual(self.posts[0]["comments"][0]["text"], "Nice post!")

    def test_comment_post_user_does_not_exist(self):
        result = comment_post(self.users, self.posts, "charlie", 1, "Hello")
        self.assertEqual(result, (False, "Only an existing user can comment on a post."))

    def test_comment_post_empty_comment(self):
        result = comment_post(self.users, self.posts, "bob", 1, "   ")
        self.assertEqual(result, (False, "Comment cannot be empty."))

    def test_comment_post_post_does_not_exist(self):
        result = comment_post(self.users, self.posts, "bob", 999, "Hello")
        self.assertEqual(result, (False, "Post 999 does not exist."))

    def test_comment_post_strips_username_and_comment(self):
        result = comment_post(self.users, self.posts, "  bob  ", 1, "  Nice post!  ")
        self.assertEqual(result, (True, "Comment added successfully to post 1."))
        self.assertEqual(self.posts[0]["comments"][0]["author"], "bob")
        self.assertEqual(self.posts[0]["comments"][0]["text"], "Nice post!")

    def test_comment_post_none_username_raises_attribute_error(self):
        with self.assertRaises(AttributeError):
            comment_post(self.users, self.posts, None, 1, "Hello")

    # -----------------------------
    # Tests for view_all_posts
    # -----------------------------

    def test_view_all_posts_success(self):
        result, visible_posts = view_all_posts(self.posts)
        self.assertTrue(result)
        self.assertEqual(len(visible_posts), 1)
        self.assertIn("Post ID: 1", visible_posts[0])
        self.assertIn("Author: alice", visible_posts[0])
        self.assertIn("Content: Hello world", visible_posts[0])
        self.assertIn("Likes: 1", visible_posts[0])
        self.assertIn("Comments: 0", visible_posts[0])

    def test_view_all_posts_no_posts(self):
        result = view_all_posts([])
        self.assertEqual(result, (False, "No posts available."))

    def test_view_all_posts_defaults_missing_likes_and_comments(self):
        posts = [
            {
                "id": 2,
                "author": "alice",
                "content": "Second post"
            }
        ]
        result, visible_posts = view_all_posts(posts)
        self.assertTrue(result)
        self.assertIn("Likes: 0", visible_posts[0])
        self.assertIn("Comments: 0", visible_posts[0])

    def test_view_all_posts_missing_required_key_raises_key_error(self):
        bad_posts = [
            {
                "author": "alice",
                "content": "Broken post"
            }
        ]
        with self.assertRaises(KeyError):
            view_all_posts(bad_posts)


if __name__ == "__main__":
    unittest.main()
