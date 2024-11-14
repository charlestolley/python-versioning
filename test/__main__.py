import pathlib
import unittest

test_dir = pathlib.Path(__file__).parent
testSuite = unittest.defaultTestLoader.discover(
    test_dir,
    pattern="[a-z]*.py",
    top_level_dir=test_dir.parent,
)

runner = unittest.TextTestRunner()
runner.run(testSuite)
