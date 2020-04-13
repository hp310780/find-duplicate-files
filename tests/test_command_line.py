import os

import pytest

import find_duplicate_files


@pytest.fixture(scope="module")
def cl_test_directory():
    return os.path.join(os.getcwd(),
                        "tests",
                        "test_directory")


@pytest.fixture(scope="module")
def cl_chunk():
    return '2'


def test_cmd_line(cl_test_directory,
                  cl_chunk):
    """Tests whether the command line parsing parses the input directory correctly.
    """
    print(find_duplicate_files.__dict__)
    parser = find_duplicate_files.parse_cmd_args(["--dir",
                                                  cl_test_directory,
                                                  "--chunk",
                                                  cl_chunk
                                                  ])
    assert parser.dir == cl_test_directory
    assert parser.chunk == int(cl_chunk)
