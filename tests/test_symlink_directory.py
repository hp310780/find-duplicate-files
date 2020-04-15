import os
import shutil

import pytest
import mock

import find_duplicate_files


@pytest.fixture(scope="module")
def directory():
    return os.path.join(os.getcwd(),
                        "tests",
                        "test_data",
                        "TestSymlink")


@pytest.fixture(scope="module")
def duplicates():
    file_1 = os.path.join(os.getcwd(),
                        "tests",
                        "test_data",
                        "TestSymlink",
                        "1.txt")
    file_2 = os.path.join(os.getcwd(),
                        "tests",
                        "test_data",
                        "TestSymlink",
                        "3",
                        "4.txt")
    return [[file_1, file_2]]


def test_find_duplicate_files_symlink_directory(directory,
                                                duplicates):
    """Tests that find_duplicate_files.find_duplicate_files accounts for
    symlinks to the current directory (avoiding infinite recursion)."""
    duplicate_files = \
        find_duplicate_files.find_duplicate_files(directory)

    assert duplicate_files == duplicates
