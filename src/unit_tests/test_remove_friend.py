import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from remove_friend import remove_friend


class TestRemoveFriend(unittest.TestCase):

    # ----- INPUT - OUTPUT TEST CASES -----

    def test_TC1_remove_friend_success(self):
        users = {"julio": {"friends": ["bob"]}, "bob": {"friends": ["julio"]}}
        self.assertEqual(
            remove_friend(users, "julio", "bob"),
            (True, "You are no longer friends with bob."),
        )

    def test_TC2_friend_user_does_not_exist(self):
        users = {"julio": {"friends": []}}
        self.assertEqual(
            remove_friend(users, "julio", "bob"),
            (False, "User 'bob' does not exist."),
        )

    def test_TC3_username_does_not_exist(self):
        users = {"bob": {"friends": []}}
        self.assertEqual(
            remove_friend(users, "julio", "bob"),
            (False, "User 'julio' does not exist."),
        )

    def test_TC4_cannot_remove_yourself(self):
        users = {"julio": {"friends": []}}
        self.assertEqual(
            remove_friend(users, "julio", "julio"),
            (False, "You cannot remove yourself."),
        )

    def test_TC5_friend_not_in_your_list(self):
        users = {"julio": {"friends": []}, "bob": {"friends": []}}
        self.assertEqual(
            remove_friend(users, "julio", "bob"),
            (False, "bob is not in your friends list."),
        )

    def test_TC6_remove_updates_both_lists(self):
        users = {"julio": {"friends": ["bob"]}, "bob": {"friends": ["julio"]}}
        remove_friend(users, "julio", "bob")
        self.assertNotIn("bob", users["julio"]["friends"])
        self.assertNotIn("julio", users["bob"]["friends"])

    # ----- EDGE CASES -----

    def test_EC1_unilateral_friendship_only_one_side_has_friend(self):
        users = {"julio": {"friends": ["bob"]}, "bob": {"friends": []}}
        self.assertEqual(
            remove_friend(users, "julio", "bob"),
            (True, "You are no longer friends with bob."),
        )
        self.assertNotIn("bob", users["julio"]["friends"])
        self.assertEqual(users["bob"]["friends"], [])

    def test_EC2_usernames_with_surrounding_whitespace(self):
        users = {"julio": {"friends": ["bob"]}, "bob": {"friends": ["julio"]}}
        self.assertEqual(
            remove_friend(users, "  julio  ", "  bob  "),
            (True, "You are no longer friends with bob."),
        )

    def test_EC3_missing_friends_keys_are_created(self):
        users = {"julio": {}, "bob": {}}
        self.assertEqual(
            remove_friend(users, "julio", "bob"),
            (False, "bob is not in your friends list."),
        )
        self.assertEqual(users["julio"]["friends"], [])
        self.assertEqual(users["bob"]["friends"], [])

    def test_EC4_remove_twice_in_a_row(self):
        users = {"julio": {"friends": ["bob"]}, "bob": {"friends": ["julio"]}}
        first = remove_friend(users, "julio", "bob")
        second = remove_friend(users, "julio", "bob")
        self.assertEqual(first, (True, "You are no longer friends with bob."))
        self.assertEqual(second, (False, "bob is not in your friends list."))

    # ----- ERROR HANDLING TESTS -----

    def test_EH1_none_username_raises_attribute_error(self):
        with self.assertRaises(AttributeError):
            remove_friend({}, None, "bob")

    def test_EH2_none_friend_username_raises_attribute_error(self):
        with self.assertRaises(AttributeError):
            remove_friend({}, "julio", None)

    def test_EH3_none_users_raises_type_error(self):
        with self.assertRaises(TypeError):
            remove_friend(None, "julio", "bob")

    def test_EH4_none_friends_list_raises_type_error(self):
        users = {"julio": {"friends": None}, "bob": {"friends": []}}
        with self.assertRaises((AttributeError, TypeError)):
            remove_friend(users, "julio", "bob")


if __name__ == '__main__':
    unittest.main()
