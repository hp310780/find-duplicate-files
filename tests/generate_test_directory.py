import os
import random

from collections import defaultdict
from typing import List


def generate_test_directory(parent_directory: str,
                            max_levels: int,
                            return_duplicates: bool = False) -> List[list]:
    """
    Generates random set of folders/files in the given parent_directory directory

    Args:
        parent_directory(str): Path to the parent_directory
        max_levels(int): Desired maximum depth of the directory tree
        return_duplicates(bool): Should this return the duplicates in the directory

    Returns:
        List: If return_duplicates is True will
              return list of lists of duplicate files in the generated directory,
              else an empty list.
    """
    if not os.path.exists(parent_directory):
        os.makedirs(parent_directory)

    root = os.getcwd()

    # Keep track of current directory to generate new folders
    os.chdir(parent_directory)

    duplicate_files = defaultdict(list)
    levels = random.randint(1, max_levels)

    for level in range(levels):
        switch = random.randint(1, max_levels)
        current_directory = os.getcwd()

        # Random switch between folder and file creation
        if switch < max_levels / 2:
            new_directory = "%s/%s" % (current_directory, level)
            os.makedirs(new_directory)
            os.chdir(new_directory)
        else:
            new_file = "%s/%s.txt" % (current_directory, level)

            with open(new_file, "w+") as f:
                for line_no in range(switch):
                    f.write("This is line %d\r\n" % (line_no + 1))

            duplicate_files[switch].append(new_file)

    os.chdir(root)

    duplicates = []
    if return_duplicates:
        for duplicate_file in duplicate_files:
            # Eliminate unique files (i.e. Only 1 exists)
            if len(duplicate_files[duplicate_file]) > 1:
                duplicates.append(duplicate_files[duplicate_file])
        return sorted(duplicates)
    return []
