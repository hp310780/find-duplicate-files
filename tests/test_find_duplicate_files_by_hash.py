import os

import pytest

import find_duplicate_files


@pytest.fixture(scope="module")
def test_file_1():
    return os.path.join(os.getcwd(),
                        "tests",
                        "test_data",
                        "TestFindDuplicateFilesByHash",
                        "1.txt")


@pytest.fixture(scope="module")
def test_file_2():
    return os.path.join(os.getcwd(),
                        "tests",
                        "test_data",
                        "TestFindDuplicateFilesByHash",
                        "2.txt")


@pytest.fixture(scope="module")
def test_file_3():
    return os.path.join(os.getcwd(),
                        "tests",
                        "test_data",
                        "TestFindDuplicateFilesByHash",
                        "3.txt")


@pytest.fixture(scope="module")
def test_file_4():
    return os.path.join(os.getcwd(),
                        "tests",
                        "test_data",
                        "TestFindDuplicateFilesByHash",
                        "4.txt")


@pytest.fixture(scope="module")
def test_file_5():
    return os.path.join(os.getcwd(),
                        "tests",
                        "test_data",
                        "TestFindDuplicateFilesByHash",
                        "5.txt")


def test_find_duplicate_files_by_hash(test_file_1,
                                      test_file_2,
                                      test_file_3,
                                      test_file_4,
                                      test_file_5):
    """Test that find_duplicate_files.find_duplicate_files_by_hash
    returns correct list of duplicate files.
    """
    duplicate_files_by_hash = \
        find_duplicate_files.find_duplicate_files_by_hash((test_file_1,
                                                           test_file_2,
                                                           test_file_3,
                                                           test_file_4,
                                                           test_file_5),
                                                          int(29 / 4),
                                                          29)
    # pre-determined duplicates
    duplicates = [[test_file_1, test_file_3],
                  [test_file_4, test_file_5]]

    assert duplicate_files_by_hash == duplicates
