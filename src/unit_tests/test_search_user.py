import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from search_user import search_user


class TestSearchUser(unittest.TestCase):

    # ----- INPUT - OUTPUT TEST CASES -----

    def test_TC1_exact_match_single_user(self):
        users = {"julio": {"friends": []}, "bob": {"friends": []}}
        self.assertEqual(
            search_user(users, "julio"),
            (True, "1 user(s) found.", ["julio"]),
        )

    def test_TC2_partial_match(self):
        users = {"julio": {"friends": []}, "bob": {"friends": []}}
        self.assertEqual(
            search_user(users, "jul"),
            (True, "1 user(s) found.", ["julio"]),
        )

    def test_TC3_case_insensitive_search(self):
        users = {"Julio": {"friends": []}, "Bob": {"friends": []}}
        self.assertEqual(
            search_user(users, "JULIO"),
            (True, "1 user(s) found.", ["Julio"]),
        )

    def test_TC4_no_matches(self):
        users = {"julio": {"friends": []}, "bob": {"friends": []}}
        self.assertEqual(
            search_user(users, "zzz"),
            (False, "No users found matching 'zzz'.", []),
        )

    def test_TC5_multiple_matches(self):
        users = {
            "julio":  {"friends": []},
            "julian": {"friends": []},
            "bob":    {"friends": []},
        }
        success, message, matches = search_user(users, "jul")
        self.assertTrue(success)
        self.assertEqual(message, "2 user(s) found.")
        self.assertEqual(set(matches), {"julio", "julian"})

    def test_TC6_empty_query_string(self):
        users = {"julio": {"friends": []}}
        self.assertEqual(
            search_user(users, ""),
            (False, "Search query cannot be empty.", []),
        )

    # ----- EDGE CASES -----

    def test_EC1_whitespace_only_query_is_empty(self):
        users = {"julio": {"friends": []}}
        self.assertEqual(
            search_user(users, "   "),
            (False, "Search query cannot be empty.", []),
        )

    def test_EC2_empty_users_dict(self):
        self.assertEqual(
            search_user({}, "julio"),
            (False, "No users found matching 'julio'.", []),
        )

    def test_EC3_query_with_surrounding_whitespace(self):
        users = {"julio": {"friends": []}, "bob": {"friends": []}}
        self.assertEqual(
            search_user(users, "  julio  "),
            (True, "1 user(s) found.", ["julio"]),
        )

    def test_EC4_mixed_case_usernames_and_query(self):
        users = {"JuLiO": {"friends": []}, "BoB": {"friends": []}}
        self.assertEqual(
            search_user(users, "julio"),
            (True, "1 user(s) found.", ["JuLiO"]),
        )

    def test_EC5_matches_are_full_usernames_not_substrings(self):
        users = {"alicejohn": {"friends": []}, "johnny": {"friends": []}}
        _, _, matches = search_user(users, "john")
        self.assertEqual(set(matches), {"alicejohn", "johnny"})

    # ----- ERROR HANDLING TESTS -----

    def test_EH1_none_query_raises_attribute_error(self):
        users = {"julio": {"friends": []}}
        with self.assertRaises(AttributeError):
            search_user(users, None)

    def test_EH2_none_users_raises_type_error(self):
        with self.assertRaises(TypeError):
            search_user(None, "julio")

    def test_EH3_non_string_username_in_users_raises_attribute_error(self):
        users = {123: {"friends": []}}
        with self.assertRaises(AttributeError):
            search_user(users, "julio")

    def test_EH4_non_string_query_raises_attribute_error(self):
        users = {"julio": {"friends": []}}
        with self.assertRaises(AttributeError):
            search_user(users, 123)


if __name__ == '__main__':
    unittest.main()
