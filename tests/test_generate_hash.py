import os

import pytest

import find_duplicate_files


@pytest.fixture(scope="module")
def test_file():
    return os.path.join(os.getcwd(),
                        "tests",
                        "test_data",
                        "TestGenerateHash",
                        "1.txt")


@pytest.fixture(scope="module")
def file_hash():
    return "ee38caabb05595d849d9a3286ae26658"


def test_generate_hash(test_file,
                       file_hash):
    generated_hash = find_duplicate_files.generate_hash(test_file)
    assert generated_hash == file_hash
