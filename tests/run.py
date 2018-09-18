import unittest

from . import test_command_line
from . import test_find_duplicate_files
from . import test_find_duplicate_files_by_hash
from . import test_generate_hash

loader = unittest.TestLoader()
suite = unittest.TestSuite()

suite.addTests(loader.loadTestsFromModule(test_command_line))
suite.addTests(loader.loadTestsFromModule(test_find_duplicate_files))
suite.addTests(loader.loadTestsFromModule(test_find_duplicate_files_by_hash))
suite.addTests(loader.loadTestsFromModule(test_generate_hash))

runner = unittest.TextTestRunner()
result = runner.run(suite)
