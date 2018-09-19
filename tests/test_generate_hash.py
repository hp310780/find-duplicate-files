import unittest
import os

import find_duplicate_files


class TestGenerateHash(unittest.TestCase):
    '''
    Returns successful if find_duplicate_files.generate_hash returns the correct
    hash for a given file.
    '''

    def setUp(self):
        self.test_file = os.path.join(os.getcwd(),
                                      "tests",
                                      "test_data",
                                      "TestGenerateHash",
                                      "1.txt")
        self.ground_truth_hash = "ee38caabb05595d849d9a3286ae26658"

    def runTest(self):
        file_hash = find_duplicate_files.generate_hash(self.test_file)
        self.assertEqual(self.ground_truth_hash, file_hash)


if __name__ == '__main__':
    unittest.main()
