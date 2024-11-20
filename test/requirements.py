import unittest

import versioning
from versioning.requirements import *

class FailedRequirementTest(unittest.TestCase):
    def test_FailedRequirement_is_a_type_of_AssertionError(self):
        self.assertIsInstance(FailedRequirement(), AssertionError)

class RequirementsTest(unittest.TestCase):
    class Dummy:
        pass

    def setUp(self):
        self.obj = self.Dummy()
        self.interface = "arbitrary name"

    def test_register_adds_the___interfaces___attribute(self):
        register(self.obj, self.interface, "1.0.0")
        self.assertTrue(hasattr(self.obj, "__interfaces__"))

    def test_require_succeeds_for_matching_version(self):
        register(self.obj, self.interface, "1.2.0")
        require(self.obj, self.interface, "1.2")

    def test_require_succeeds_for_compatible_version(self):
        register(self.obj, self.interface, "1.5.1")
        require(self.obj, self.interface, "1.1")

    def test_require_raises_FailedRequirement_if_not_registered(self):
        self.assertRaises(
            FailedRequirement,
            require,
            self.obj,
            self.interface,
            "1.0",
        )

    def test_require_raises_FailedRequirement_for_insufficient_version(self):
        register(self.obj, self.interface, "1.2.3")
        self.assertRaises(
            FailedRequirement,
            require,
            self.obj,
            self.interface,
            "1.3",
        )

    def test_require_raises_FailedRequirement_for_wrong_major_version(self):
        register(self.obj, self.interface, "2.0.0")
        self.assertRaises(
            FailedRequirement,
            require,
            self.obj,
            self.interface,
            "1.0",
        )

    def test_an_object_may_implement_multiple_interfaces(self):
        register(self.obj, "FirstInterface", "1.2.3")
        register(self.obj, "SecondInterface", "1.9.3")
        require(self.obj, "SecondInterface", "1.8")
        require(self.obj, "FirstInterface", "1.0")

    def test_a_single_object_may_implement_two_different_major_versions(self):
        register(self.obj, self.interface, "1.3.4")
        register(self.obj, self.interface, "2.1.2")
        require(self.obj, self.interface, "1.2")
        require(self.obj, self.interface, "2.1")

class PackageVersionTest(unittest.TestCase):
    def test_package_implements_versioning_version_1_0(self):
        require(versioning, "versioning", "1.0")

if __name__ == "__main__":
    unittest.main()
