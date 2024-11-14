import unittest

from versioning.identifier import *

class VersionIdentifierTest(unittest.TestCase):
    def test_major_number_is_required(self):
        self.assertRaises(TypeError, VersionIdentifier)

    def test_minor_patch_and_edition_default_to_zero(self):
        self.assertEqual(VersionIdentifier(1), VersionIdentifier(1, 0, 0, 0))

    def test_constructor_raises_ValueError_for_negative_number(self):
        self.assertRaises(ValueError, VersionIdentifier, -1)
        self.assertRaises(ValueError, VersionIdentifier, 1, -1)
        self.assertRaises(ValueError, VersionIdentifier, 1, 2, -1)
        self.assertRaises(ValueError, VersionIdentifier, 1, 2, 3, -1)

    def test_numbers_are_called_major_minor_patch_edition(self):
        version = VersionIdentifier(1, 2, 3, 4)
        self.assertEqual(version.major, 1)
        self.assertEqual(version.minor, 2)
        self.assertEqual(version.patch, 3)
        self.assertEqual(version.edition, 4)

    def test_parse_converts_str_to_VersionIdentifier(self):
        self.assertEqual(
            VersionIdentifier.parse("1.2.3.4"),
            VersionIdentifier(1, 2, 3, 4),
        )

    def test_parse_raises_ValueError_for_empty_string(self):
        self.assertRaises(ValueError, VersionIdentifier.parse, "")

    def test_parse_raises_ValueError_for_non_integers(self):
        self.assertRaises(ValueError, VersionIdentifier.parse, "example.com")

    def test_parse_raises_ValueError_for_too_many_numbers(self):
        self.assertRaises(ValueError, VersionIdentifier.parse, "1.2.3.4.5")

    def test_parse_accepts_fewer_numbers(self):
        self.assertEqual(
            VersionIdentifier.parse("3.2.1"),
            VersionIdentifier(3, 2, 1, 0),
        )

    def test_VersionIdentifier_can_be_used_as_a_dict_key(self):
        things = {}
        things[VersionIdentifier(1)] = "thing v1"
        things[VersionIdentifier(2)] = "thing v2"

        self.assertEqual(things[VersionIdentifier.parse("1.0.0")], "thing v1")
        self.assertEqual(things[VersionIdentifier.parse("2.0.0")], "thing v2")

    def test_eval_repr_produces_an_equivalent_object(self):
        version = VersionIdentifier(2, 4, 6, 8)
        self.assertEqual(eval(repr(version)), version)

    def test_str_is_the_reverse_of_parse(self):
        version = VersionIdentifier(8, 6, 4, 2)
        self.assertEqual(VersionIdentifier.parse(str(version)), version)

if __name__ == "__main__":
    unittest.main()
