import os
import shutil

from timeit import default_timer as timer

import find_duplicate_files
from tests import generate_test_directory


def run():
    '''
    Output time taken for a full hash vs chunked hash
    '''
    # Generate random test directory tree with max_levels 1000
    directory = os.path.join(os.getcwd(), "test_folder")
    duplicates = generate_test_directory.generate_test_directory(directory,
                                                                 1000,
                                                                 True)

    start = timer()
    duplicate_files_full = find_duplicate_files.find_duplicate_files(directory,
                                                                     1)
    end = timer()
    full_hash_time = end - start

    # Arbitrary chunk size of 3 to compare.
    start = timer()
    duplicate_files_chunk = find_duplicate_files.find_duplicate_files(
        directory, 3)
    end = timer()
    chunk_hash_time = end - start

    if duplicate_files_full == duplicates:
        print("Method 1 - Generate full hash returns correct duplicates."
              "Time %s" % (
                  full_hash_time))

    if duplicate_files_chunk == duplicates:
        print("Method 2 - Generate chunked hash returns correct duplicates."
              "Time %s" % (
                  chunk_hash_time))

    shutil.rmtree(directory)


if __name__ == '__main__':
    run()
