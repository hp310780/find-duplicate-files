import os
import shutil

import pytest
import mock

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
    """Tests that find-duplicate-files.find-duplicate-files returns
       the duplicate files in the given directory."""
    duplicate_files = \
        find_duplicate_files.find_duplicate_files(parent_directory)

    assert duplicate_files == duplicates


def test_logs_missing_directory():
    """Tests that a missing directory is correctly captured."""
    missing_dir = "missing/directory"

    with pytest.raises(ValueError):
        find_duplicate_files.find_duplicate_files(missing_dir)


@mock.patch("os.path.getsize", side_effect=OSError)
@mock.patch("logging.warning")
def test_logs_file_size_warning(mock_logging,
                                mock_getsize):
    """Tests an os.stat error is logged and captured correctly."""
    directory = os.path.join(os.getcwd(),
                             "tests",
                             "test_data",
                             "TestMissingFile")

    f = os.path.join(os.getcwd(),
                     "tests",
                     "test_data",
                     "TestMissingFile",
                     "1.txt")

    find_duplicate_files.find_duplicate_files(directory)

    mock_logging.assert_called_once_with(f"Could not stat: {f}. Skipping. ")
