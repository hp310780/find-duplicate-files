import unittest
import os

import find_duplicate_files


class TestCommandLine(unittest.TestCase):
    '''
    Returns successful if the command line arguments parsing
    parses the input directory correctly
    '''

    def setUp(self):
        self.ground_truth_directory = os.path.join(os.getcwd(),
                                                   "tests",
                                                   "test_directory")

        self.ground_truth_chunk = 2

    def runTest(self):
        parser = find_duplicate_files.parse_cmd_args(["--dir",
                                                      self.ground_truth_directory,
                                                      "--chunk",
                                                      str(
                                                          self.ground_truth_chunk)])
        self.assertEqual(parser.dir, self.ground_truth_directory)
        self.assertEqual(parser.chunk, self.ground_truth_chunk)


if __name__ == '__main__':
    unittest.main()
