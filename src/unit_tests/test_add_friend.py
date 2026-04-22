import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from add_friend import add_friend


class TestAddFriend(unittest.TestCase):

    # ----- INPUT - OUTPUT TEST CASES -----

    def test_TC1_add_friend_both_have_empty_friends_list(self):
        users = {"julio": {"friends": []}, "bob": {"friends": []}}
        self.assertEqual(
            add_friend(users, "julio", "bob"),
            (True, "bob added as a friend successfully."),
        )

    def test_TC2_add_friend_user_has_other_friends(self):
        users = {"julio": {"friends": ["charlie"]}, "bob": {"friends": []}}
        self.assertEqual(
            add_friend(users, "julio", "bob"),
            (True, "bob added as a friend successfully."),
        )

    def test_TC3_friend_user_does_not_exist(self):
        users = {"julio": {"friends": []}}
        self.assertEqual(
            add_friend(users, "julio", "bob"),
            (False, "User 'bob' does not exist."),
        )

    def test_TC4_username_does_not_exist(self):
        users = {"bob": {"friends": []}}
        self.assertEqual(
            add_friend(users, "julio", "bob"),
            (False, "User 'julio' does not exist."),
        )

    def test_TC5_cannot_add_yourself(self):
        users = {"julio": {"friends": []}}
        self.assertEqual(
            add_friend(users, "julio", "julio"),
            (False, "You cannot add yourself as a friend."),
        )

    def test_TC6_already_a_friend(self):
        users = {"julio": {"friends": ["bob"]}, "bob": {"friends": ["julio"]}}
        self.assertEqual(
            add_friend(users, "julio", "bob"),
            (False, "bob is already a friend."),
        )

    # ----- EDGE CASES -----

    def test_EC1_missing_friends_keys_are_created(self):
        users = {"julio": {}, "bob": {}}
        add_friend(users, "julio", "bob")
        self.assertIn("friends", users["julio"])
        self.assertIn("friends", users["bob"])
        self.assertIn("bob", users["julio"]["friends"])
        self.assertIn("julio", users["bob"]["friends"])

    def test_EC2_empty_friends_lists_success(self):
        users = {"julio": {"friends": []}, "bob": {"friends": []}}
        self.assertEqual(
            add_friend(users, "julio", "bob"),
            (True, "bob added as a friend successfully."),
        )

    def test_EC3_different_users_oscar_and_juan(self):
        users = {"Oscar": {"friends": []}, "Juan": {"friends": []}}
        self.assertEqual(
            add_friend(users, "Oscar", "Juan"),
            (True, "Juan added as a friend successfully."),
        )

    def test_EC4_bidirectional_friendship(self):
        users = {"julio": {"friends": []}, "bob": {"friends": []}}
        add_friend(users, "julio", "bob")
        self.assertIn("bob", users["julio"]["friends"])
        self.assertIn("julio", users["bob"]["friends"])

    # ----- ERROR HANDLING TESTS -----

    def test_EH1_none_username_raises_attribute_error(self):
        with self.assertRaises(AttributeError):
            add_friend({}, None, "bob")

    def test_EH2_none_friend_username_raises_attribute_error(self):
        with self.assertRaises(AttributeError):
            add_friend({}, "julio", None)

    def test_EH3_none_users_raises_type_error(self):
        with self.assertRaises(TypeError):
            add_friend(None, "julio", "bob")

    def test_EH4_none_friends_list_raises_error(self):
        users = {"julio": {"friends": None}, "bob": {"friends": []}}
        with self.assertRaises((AttributeError, TypeError)):
            add_friend(users, "julio", "bob")


if __name__ == '__main__':
    unittest.main()
