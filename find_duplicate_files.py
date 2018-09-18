import os
import sys
import hashlib
import logging
import argparse
import math

from collections import defaultdict


def generate_hash(file_path,
                  chunk_size=1024,
                  seek_file_at=0):
    '''
    Generates md5 hash for file chunk

    Args:
        file_path(str): Path to file to generate hash for
        chunk_size(int): Hash size to read
        previous_chunk_size(int): Where to read the file from in bytes

    Returns:
        Str: Hexdigit digest of file hash
    '''
    with open(file_path, 'rb') as file_to_hash:
        md5_hash = hashlib.md5()
        buffer = file_to_hash.read(chunk_size)

        if seek_file_at != 0:
            file_to_hash.seek(seek_file_at)

        while len(buffer) > 0:
            md5_hash.update(buffer)
            buffer = file_to_hash.read(chunk_size)

    return md5_hash.hexdigest()


def find_duplicate_files_by_hash(files,
                                 hash_chunk_size,
                                 file_size,
                                 previous_chunk_size=0):
    '''
    Given files of the same size, recursively check
    the incremental hash of the files to find duplicates

    Args:
        files(list): List of files to generate hashes for
        hash_chunk_size(int): Size of hash chunk
        previous_chunk_size(int): Cumulative file pointer in bytes
        file_size(int): The file size for this list of files

    Returns:
        List: List of duplicate files given the original list of files
    '''
    file_hashes = defaultdict(list)

    for file_path in files:
        try:
            file_hash = generate_hash(file_path,
                                      hash_chunk_size,
                                      previous_chunk_size)
        except IOError as e:
            logging.error("Could not read: %s. Exiting." %
                          (file_path))
            raise e

        file_hashes[file_hash].append(file_path)

    previous_chunk_size = hash_chunk_size
    hash_chunk_size = file_size - hash_chunk_size
    full_file_hashes = defaultdict(list)

    for file_hash in file_hashes:
        if len(file_hashes[file_hash]) > 1:

            for file_path in file_hashes[file_hash]:
                # most likely have a match
                try:
                    full_file_hash = generate_hash(file_path,
                                                   hash_chunk_size,
                                                   previous_chunk_size)
                except IOError as e:
                    logging.error("Could not read: %s. Exiting." %
                                  (file_path))
                    raise e

                full_file_hashes[full_file_hash].append(file_path)

            for full_file_hash in full_file_hashes:
                if len(full_file_hashes[full_file_hash]) > 1:
                    return full_file_hashes[full_file_hash]


def find_duplicate_files(directory_to_search, chunks=1):
    '''
    Finds duplicate files in the given directory.

    First, find files of the same size (indicating similar contents).
    Then compare hashes of successive file chunks,
    eliminating any differing files.

    Args:
        directory_to_search(str): Path to the parent directory to search
        chunks(int): No. of chunks to generate per file

    Returns:
        List of Lists: List of lists of duplicate files in the directory tree
    '''
    if not os.path.exists(directory_to_search):
        raise ValueError("Given directory %s does not seem to exist." % (
            directory_to_search))

    file_sizes = defaultdict(list)

    # followlinks in order to return any symlinked files
    for root, dirs, files in os.walk(directory_to_search, followlinks=True):
        for file in files:
            file_path = os.path.join(root, file)
            file_size = None
            # Duplicates will have the same file size
            try:
                file_size = os.path.getsize(file_path)
            except OSError as e:
                # Account for permission errors etc.
                logging.warning("Could not stat: %s. Skipping. %s"
                                % (file_path, e))
                continue

            file_sizes[file_size].append(file_path)

    duplicate_files = []
    # Inspect contents of all same size files to determine if duplicates
    for file_size in file_sizes:
        # Eliminate any unique files
        if len(file_sizes[file_size]) > 1 and file_size > 0:
            # Find the hash chunk size. 1 is full file, 4 is a quarter etc.
            hash_chunk_size = int(math.ceil(file_size / chunks))
            duplicates = find_duplicate_files_by_hash(file_sizes[file_size],
                                                      hash_chunk_size,
                                                      file_size)
            if duplicates:
                duplicate_files.append(duplicates)
        # No need to check empty files
        elif file_size == 0:
            duplicate_files.append(file_sizes[file_size])

    return sorted(duplicate_files)


def parse_cmd_args(args):
    '''
    Parse command line arguments into stored types

    Args:
        args(list[(str)]): List of arguments from command line

    Returns:
        Object with parsed arguments with correct type
    '''
    parser = argparse.ArgumentParser(
        description='Find duplicates files in the given directory')

    # The only argument expected is the directory to search
    parser.add_argument('--dir',
                        type=str,
                        required=True,
                        help='Path of the parent directory to search')
    parser.add_argument('--chunk',
                        type=int,
                        default=1,
                        help='Optional: Size of initial hash to check.'
                             '1 indicates the full file hash. 2 is half etc.')

    parsed_args = parser.parse_args(args)
    return parsed_args


if __name__ == '__main__':
    from pprint import pprint
    from timeit import default_timer as timer

    args = parse_cmd_args(sys.argv[1:])

    duplicates = find_duplicate_files(args.dir, args.chunk)
    print("Duplicate files found in %s -" % (args.dir))
    pprint(duplicates)
