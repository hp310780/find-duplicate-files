import os

import mock
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
    duplicate_files_by_hash = \
        find_duplicate_files.find_duplicate_files_by_hash([test_file_1,
                                                           test_file_2,
                                                           test_file_3,
                                                           test_file_4,
                                                           test_file_5],
                                                          int(29 / 4),
                                                          29)
    # pre-determined duplicates
    duplicates = [[test_file_1, test_file_3],
                  [test_file_4, test_file_5]]

    assert duplicate_files_by_hash == duplicates


def test_generate_hash_io_error_raised():
    files = ["1.txt"]
    hash_chunk_size = 1
    file_size = 1

    with pytest.raises(IOError):
        find_duplicate_files.find_duplicate_files_by_hash(files,
                                                          hash_chunk_size,
                                                          file_size)


def mock_generate_hash(*args, **kwargs):
    file_path, hash_chunk_size, file_pointer_at = args

    if file_pointer_at == 0:
        return "hash0"

    if hash_chunk_size == 28:
        raise IOError


@mock.patch("find_duplicate_files.generate_hash", side_effect=mock_generate_hash)
def test_full_file_hash_error_is_raised(mock_hash):
    file_1 = os.path.join(os.getcwd(),
                          "tests",
                          "test_data",
                          "TestGenerateHashErrors",
                          "1.txt")
    file_2 = os.path.join(os.getcwd(),
                          "tests",
                          "test_data",
                          "TestGenerateHashErrors",
                          "2.txt")
    files = [file_1, file_2]
    hash_chunk_size = 1
    file_size = 29

    with pytest.raises(IOError):
        find_duplicate_files.find_duplicate_files_by_hash(files,
                                                          hash_chunk_size,
                                                          file_size)
