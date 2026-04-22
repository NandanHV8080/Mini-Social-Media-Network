import os
import sys
import unittest

# Allow imports from src/
sys.path.append(os.path.abspath("src"))

from posts import create_post
from delete_post import delete_post
from like_post import like_post


class TestPostsLike(unittest.TestCase):

    def setUp(self):
        self.users = {
            "alice": {
                "password": "123",
                "friends": [],
                "posts": [1]
            },
            "bob": {
                "password": "456",
                "friends": [],
                "posts": []
            }
        }

        self.posts = [
            {
                "id": 1,
                "author": "alice",
                "content": "Hello world",
                "likes": [],
                "comments": []
            }
        ]

    # -----------------------------
    # Tests for create_post
    # -----------------------------

    def test_create_post_success(self):
        result = create_post(self.users, self.posts, "alice", "New post")
        self.assertEqual(result, (True, "Post 2 created successfully."))
        self.assertEqual(len(self.posts), 2)
        self.assertEqual(self.posts[-1]["id"], 2)
        self.assertEqual(self.posts[-1]["author"], "alice")
        self.assertEqual(self.posts[-1]["content"], "New post")
        self.assertEqual(self.users["alice"]["posts"], [1, 2])

    def test_create_post_user_does_not_exist(self):
        result = create_post(self.users, self.posts, "charlie", "Hello")
        self.assertEqual(result, (False, "Only an existing user can create a post."))

    def test_create_post_empty_content(self):
        result = create_post(self.users, self.posts, "alice", "   ")
        self.assertEqual(result, (False, "Post content cannot be empty."))

    def test_create_post_strips_author_and_content(self):
        result = create_post(self.users, self.posts, "  alice  ", "  Nice post  ")
        self.assertEqual(result, (True, "Post 2 created successfully."))
        self.assertEqual(self.posts[-1]["author"], "alice")
        self.assertEqual(self.posts[-1]["content"], "Nice post")

    def test_create_post_none_author_raises_attribute_error(self):
        with self.assertRaises(AttributeError):
            create_post(self.users, self.posts, None, "Hello")

    # -----------------------------
    # Tests for delete_post
    # -----------------------------

    def test_delete_post_success(self):
        result = delete_post(self.users, self.posts, "alice", 1)
        self.assertEqual(result, (True, "Post 1 deleted successfully."))
        self.assertEqual(self.posts, [])
        self.assertEqual(self.users["alice"]["posts"], [])

    def test_delete_post_user_does_not_exist(self):
        result = delete_post(self.users, self.posts, "charlie", 1)
        self.assertEqual(result, (False, "Only an existing user can delete a post."))

    def test_delete_post_cannot_delete_others_post(self):
        result = delete_post(self.users, self.posts, "bob", 1)
        self.assertEqual(result, (False, "You can only delete your own posts."))

    def test_delete_post_post_does_not_exist(self):
        result = delete_post(self.users, self.posts, "alice", 99)
        self.assertEqual(result, (False, "Post 99 does not exist."))

    def test_delete_post_strips_author(self):
        result = delete_post(self.users, self.posts, "  alice  ", 1)
        self.assertEqual(result, (True, "Post 1 deleted successfully."))

    def test_delete_post_none_author_raises_attribute_error(self):
        with self.assertRaises(AttributeError):
            delete_post(self.users, self.posts, None, 1)

    # -----------------------------
    # Tests for like_post
    # -----------------------------

    def test_like_post_success(self):
        result = like_post(self.users, self.posts, "bob", 1)
        self.assertEqual(result, (True, "Post 1 liked successfully."))
        self.assertIn("bob", self.posts[0]["likes"])

    def test_like_post_user_does_not_exist(self):
        result = like_post(self.users, self.posts, "charlie", 1)
        self.assertEqual(result, (False, "Only an existing user can like a post."))

    def test_like_post_post_does_not_exist(self):
        result = like_post(self.users, self.posts, "bob", 99)
        self.assertEqual(result, (False, "Post 99 does not exist."))

    def test_like_post_duplicate_like_blocked(self):
        self.posts[0]["likes"].append("bob")
        result = like_post(self.users, self.posts, "bob", 1)
        self.assertEqual(result, (False, "User bob has already liked post 1."))

    def test_like_post_strips_username(self):
        result = like_post(self.users, self.posts, "  bob  ", 1)
        self.assertEqual(result, (True, "Post 1 liked successfully."))
        self.assertIn("bob", self.posts[0]["likes"])

    def test_like_post_none_username_raises_attribute_error(self):
        with self.assertRaises(AttributeError):
            like_post(self.users, self.posts, None, 1)


if __name__ == "__main__":
    unittest.main()
