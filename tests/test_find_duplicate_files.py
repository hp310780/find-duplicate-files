import os
import shutil

import pytest

import find_duplicate_files
import generate_test_directory as generator


@pytest.fixture(scope="function")
def parent_directory():
    parent_directory = os.path.join(os.getcwd(),
                                    "tests",
                                    "test_directory")
    yield parent_directory
    shutil.rmtree(parent_directory)


@pytest.fixture(scope="function")
def duplicates(parent_directory):
    return generator.generate_test_directory(parent_directory, 100, True)


def test_find_duplicate_files(parent_directory,
                              duplicates):
    """Tests that find_duplicate_files.find_duplicate_files returns
       the duplicate files in the given directory."""
    duplicate_files = \
        find_duplicate_files.find_duplicate_files(parent_directory)

    assert duplicate_files == duplicates
