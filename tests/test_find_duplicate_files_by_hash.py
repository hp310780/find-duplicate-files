import unittest
import os

import find_duplicate_files


class TestFindDuplicateFilesByHash(unittest.TestCase):
    '''
    Returns successful if find_duplicate_files.find_duplicate_files_by_hash returns
    the correct list of duplicate files given a test directory of three identically sized
    files with differing contents.
    '''
    def setUp(self):
        test_file_1 = os.path.join(os.getcwd(),
                                   "tests",
                                   "test_data",
                                   "TestFindDuplicateFilesByHash",
                                   "1.txt")
        test_file_2 = os.path.join(os.getcwd(),
                                   "tests",
                                   "test_data",
                                   "TestFindDuplicateFilesByHash",
                                   "2.txt")
        test_file_3 = os.path.join(os.getcwd(),
                                   "tests",
                                   "test_data",
                                   "TestFindDuplicateFilesByHash",
                                   "3.txt")
        # 3 files of equal size. 2.txt has differing content
        self.test_files = [test_file_1, test_file_2, test_file_3]
        self.ground_truth_duplicates = [test_file_1, test_file_3]

    def runTest(self):
        duplicate_files_by_hash = \
            find_duplicate_files.find_duplicate_files_by_hash(self.test_files,
                                                              int(29 / 4),
                                                              29)
        self.assertEqual(self.ground_truth_duplicates, duplicate_files_by_hash)


if __name__ == '__main__':
    unittest.main()
