import unittest
import os
import shutil

import find_duplicate_files

from . import generate_test_directory as generator


class TestFindDuplicateFiles(unittest.TestCase):
    '''
    Returns successful if find_duplicate_files.find_duplicate_files returns
    the duplicate files in the given directory.
    '''

    def setUp(self):
        self.parent_directory = os.path.join(os.getcwd(),
                                             "tests",
                                             "test_directory")
        self.ground_truth_duplicates = \
            generator.generate_test_directory(self.parent_directory, 100, True)

    def tearDown(self):
        shutil.rmtree(self.parent_directory)

    def runTest(self):
        duplicate_files = \
            find_duplicate_files.find_duplicate_files(self.parent_directory)

        self.assertEqual(duplicate_files, self.ground_truth_duplicates)


if __name__ == '__main__':
    unittest.main()
