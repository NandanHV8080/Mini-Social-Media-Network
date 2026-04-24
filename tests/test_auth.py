import os
import sys
import unittest

# Allow imports from src/
sys.path.append(os.path.abspath("src"))

from create_user import create_user
from delete_account import delete_account
from login_logout import login_user, logout_user


class TestAuth(unittest.TestCase):

    def setUp(self):
        self.users = {
            "alice": {
                "password": "123",
                "friends": ["bob"],
                "posts": [1]
            },
            "bob": {
                "password": "456",
                "friends": ["alice"],
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
    # Tests for create_user
    # -----------------------------

    def test_create_user_success(self):
        result = create_user(self.users, "charlie", "789")
        self.assertEqual(result, (True, "Account created for charlie."))
        self.assertIn("charlie", self.users)
        self.assertEqual(self.users["charlie"]["password"], "789")
        self.assertEqual(self.users["charlie"]["friends"], [])
        self.assertEqual(self.users["charlie"]["posts"], [])

    def test_create_user_existing_user(self):
        result = create_user(self.users, "alice", "999")
        self.assertEqual(result, (False, "User already exists."))

    def test_create_user_empty_username(self):
        result = create_user(self.users, "   ", "123")
        self.assertEqual(result, (False, "Username cannot be empty."))

    def test_create_user_empty_password(self):
        result = create_user(self.users, "charlie", "")
        self.assertEqual(result, (False, "Password cannot be empty."))

    def test_create_user_strips_username(self):
        result = create_user(self.users, "  charlie  ", "789")
        self.assertEqual(result, (True, "Account created for charlie."))
        self.assertIn("charlie", self.users)

    def test_create_user_none_username_raises_attribute_error(self):
        with self.assertRaises(AttributeError):
            create_user(self.users, None, "123")

    # -----------------------------
    # Tests for delete_account
    # -----------------------------

    def test_delete_account_success(self):
        current_user = "alice"
        result = delete_account(self.users, "alice", current_user, self.posts)

        self.assertEqual(
            result,
            (True, "Account alice deleted successfully.", None)
        )
        self.assertNotIn("alice", self.users)
        self.assertEqual(self.posts, [])
        self.assertNotIn("alice", self.users["bob"]["friends"])

    def test_delete_account_user_does_not_exist(self):
        result = delete_account(self.users, "charlie", None, self.posts)
        self.assertEqual(result, (False, "User does not exist.", None))

    def test_delete_account_empty_username(self):
        result = delete_account(self.users, "   ", None, self.posts)
        self.assertEqual(result, (False, "Username cannot be empty.", None))

    def test_delete_account_not_current_user(self):
        current_user = "bob"
        result = delete_account(self.users, "alice", current_user, self.posts)
        self.assertEqual(
            result,
            (True, "Account alice deleted successfully.", "bob")
        )

    def test_delete_account_without_posts_list(self):
        result = delete_account(self.users, "alice", "alice", None)
        self.assertEqual(
            result,
            (True, "Account alice deleted successfully.", None)
        )
        self.assertNotIn("alice", self.users)

    def test_delete_account_none_username_raises_attribute_error(self):
        with self.assertRaises(AttributeError):
            delete_account(self.users, None, None, self.posts)

    # -----------------------------
    # Tests for login_user
    # -----------------------------

    def test_login_user_success(self):
        result = login_user(self.users, "alice", "123")
        self.assertEqual(result, (True, "alice logged in successfully."))

    def test_login_user_wrong_password(self):
        result = login_user(self.users, "alice", "999")
        self.assertEqual(result, (False, "Incorrect password."))

    def test_login_user_user_does_not_exist(self):
        result = login_user(self.users, "charlie", "123")
        self.assertEqual(result, (False, "User does not exist."))

    def test_login_user_empty_username(self):
        result = login_user(self.users, "   ", "123")
        self.assertEqual(result, (False, "Username cannot be empty."))

    def test_login_user_strips_username(self):
        result = login_user(self.users, "  alice  ", "123")
        self.assertEqual(result, (True, "alice logged in successfully."))

    def test_login_user_none_username_raises_attribute_error(self):
        with self.assertRaises(AttributeError):
            login_user(self.users, None, "123")

    # -----------------------------
    # Tests for logout_user
    # -----------------------------

    def test_logout_user_success(self):
        result = logout_user("alice")
        self.assertEqual(result, (None, "alice logged out successfully."))

    def test_logout_user_none(self):
        result = logout_user(None)
        self.assertEqual(result, (None, "No user is currently logged in."))


if __name__ == "__main__":
    unittest.main()
