import unittest

from versioning.numbers import *

class VersionTest(unittest.TestCase):
    def test_major_number_is_required(self):
        self.assertRaises(TypeError, Version)

    def test_minor_and_patch_default_to_zero(self):
        self.assertEqual(Version(1), Version(1, 0, 0))

    def test_constructor_raises_ValueError_for_negative_number(self):
        self.assertRaises(ValueError, Version, -1)
        self.assertRaises(ValueError, Version, 1, -1)
        self.assertRaises(ValueError, Version, 1, 2, -1)

    def test_numbers_are_called_major_minor_patch(self):
        version = Version(1, 2, 3)
        self.assertEqual(version.major, 1)
        self.assertEqual(version.minor, 2)
        self.assertEqual(version.patch, 3)

    def test_not_equal_to_objects_of_other_types(self):
        self.assertNotEqual(Version(1), 1)

    def test_not_less_than_equal_Version(self):
        self.assertFalse(Version(1, 5, 9) < Version(1, 5, 9))

    def test_less_than_Version_with_higher_major_number(self):
        self.assertTrue(Version(1, 5, 9) < Version(2, 5, 9))
        self.assertTrue(Version(2, 5, 9) < Version(3))

    def test_not_less_than_Version_with_lower_major_number(self):
        self.assertFalse(Version(2) < Version(1, 5, 9))
        self.assertFalse(Version(2, 4) < Version(1, 5, 9))
        self.assertFalse(Version(2, 5, 8) < Version(1, 5, 9))

    def test_less_than_Version_with_equal_major_but_higher_minor_number(self):
        self.assertTrue(Version(1, 5, 9) < Version(1, 6, 9))
        self.assertTrue(Version(1, 6, 9) < Version(1, 7))

    def test_not_less_than_Version_w_equal_major_but_lower_minor_number(self):
        self.assertFalse(Version(1, 6) < Version(1, 5, 9))
        self.assertFalse(Version(1, 6, 8) < Version(1, 5, 9))

    def test_less_than_Version_with_equal_minor_but_higher_patch_number(self):
        self.assertTrue(Version(1, 5, 9) < Version(1, 5, 10))

    def test_not_less_than_Version_w_equal_minor_but_lower_patch_number(self):
        self.assertFalse(Version(1, 5, 10) < Version(1, 5, 9))

    def test_parse_converts_str_to_Version(self):
        self.assertEqual(Version.parse("1.2.3"), Version(1, 2, 3))

    def test_parse_raises_ValueError_for_empty_string(self):
        self.assertRaises(ValueError, Version.parse, "")

    def test_parse_raises_ValueError_for_non_integers(self):
        self.assertRaises(ValueError, Version.parse, "example.com")

    def test_parse_raises_ValueError_for_too_many_numbers(self):
        self.assertRaises(ValueError, Version.parse, "1.2.3.4")

    def test_parse_accepts_fewer_numbers(self):
        self.assertEqual(Version.parse("3.2"), Version(3, 2, 0))

    def test_Version_can_be_used_as_a_dict_key(self):
        things = {}
        things[Version(1)] = "thing v1"
        things[Version(2)] = "thing v2"

        self.assertEqual(things[Version.parse("1.0.0")], "thing v1")
        self.assertEqual(things[Version.parse("2.0.0")], "thing v2")

    def test_eval_repr_produces_an_equivalent_object(self):
        version = Version(2, 4, 6)
        self.assertEqual(eval(repr(version)), version)

    def test_str_is_the_reverse_of_parse(self):
        version = Version(8, 6, 4)
        self.assertEqual(Version.parse(str(version)), version)

if __name__ == "__main__":
    unittest.main()
