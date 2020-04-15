#!/usr/bin/env python3.6

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
        seek_file_at(int): Where to read the file from in bytes

    Returns:
        Str: Hexdigit digest of file hash
    '''
    md5_hash = hashlib.md5()

    with open(file_path, 'rb') as file_to_hash:
        if seek_file_at != 0:
            file_to_hash.seek(seek_file_at)

        buffer = file_to_hash.read(chunk_size)
        md5_hash.update(buffer)

    return md5_hash.hexdigest()


def find_duplicate_files_by_hash(files,
                                 hash_chunk_size,
                                 file_size,
                                 file_pointer_at=0):
    '''
    Given files of the same size, recursively check
    the incremental hash of the files to find duplicates

    Args:
        files(list): List of files to generate hashes for
        hash_chunk_size(int): Size of hash chunk
        file_size(int): The file size for this list of files
        file_pointer_at(int): Cumulative file pointer in bytes


    Returns:
        List: List of duplicate files given the original list of files
    '''
    file_hashes = defaultdict(list)

    for file_path in files:
        try:
            file_hash = generate_hash(file_path,
                                      hash_chunk_size,
                                      file_pointer_at)
        except IOError as e:
            logging.error("Could not read: %s. Exiting." %
                          file_path)
            raise e

        file_hashes[file_hash].append(file_path)

    file_pointer_at = hash_chunk_size
    hash_chunk_size = file_size - hash_chunk_size
    full_file_hashes = defaultdict(list)
    duplicates = []

    # Indicates chunk size of 1 and thus we don't need to compute full hash
    if file_pointer_at == file_size:
        full_file_hashes = file_hashes
    else:
        for file_hash in file_hashes:
            if len(file_hashes[file_hash]) > 1:

                for file_path in file_hashes[file_hash]:
                    # most likely have a match
                    try:
                        full_file_hash = generate_hash(file_path,
                                                       hash_chunk_size,
                                                       file_pointer_at)
                    except IOError as e:
                        logging.error("Could not read: %s. Exiting." %
                                      (file_path))
                        raise e

                    full_file_hashes[full_file_hash].append(file_path)

    for full_file_hash in full_file_hashes:
        if len(full_file_hashes[full_file_hash]) > 1:
            duplicates.append(full_file_hashes[full_file_hash])

    return duplicates


def directory_key(directory):
    """
    Gets key information for a directory.
    
    Arguments:
        directory (str): Directory to get key for
    """
    dirstat = os.stat(directory)
    return dirstat.st_dev, dirstat.st_ino


def find_duplicate_files(directory_to_search, chunks=1):
    '''
    Finds duplicate files in the given directory.

    First, resolve symlinks and check for self references,
    then find files of the same size (indicating similar contents).
    Then compare hashes of first file chunk then full hash if the first
    chunk matches.

    Args:
        directory_to_search(str): Path to the parent directory to search
        chunks(int): Size of chunk to generate per file

    Returns:
        List of Lists: List of lists of duplicate files in the directory tree
    '''
    if not os.path.exists(directory_to_search):
        raise ValueError("Given directory %s does not seem to exist." % (
            directory_to_search))

    file_sizes = defaultdict(list)
    seen = set()

    for root, dirs, files in os.walk(directory_to_search, followlinks=True):
        # To avoid cyclic symlinks crashing the program, seen will keep track of seen directories
        seen.add(directory_key(root))
        directories_to_search = []
        for d in dirs:
            dirpath = os.path.realpath(os.path.join(root, d))
            dirkey = directory_key(dirpath)
            if dirkey not in seen:
                seen.add(dirkey)
                directories_to_search.append(d)
        # Amend in place
        dirs[:] = directories_to_search

        for f in files:
            file_path = os.path.join(root, f)
            file_size = None
            try:
                file_size = os.path.getsize(file_path)
            except OSError as e:
                logging.warning("Could not stat: %s. Skipping. %s"
                                % (file_path, e))
                continue
            file_sizes[file_size].append(file_path)

    duplicate_files = []
    # Inspect contents of all same size files to determine if duplicates
    for file_size in file_sizes:
        # Only check files where more than 1 exists of the same size
        if len(file_sizes[file_size]) > 1 and file_size > 0:
            # Find the hash chunk size. 1 is full file, 4 is a quarter etc.
            hash_chunk_size = int(math.ceil(file_size / chunks))
            duplicates = find_duplicate_files_by_hash(file_sizes[file_size],
                                                      hash_chunk_size,
                                                      file_size)
            if duplicates:
                for d in duplicates:
                    duplicate_files.append(d)

        # No need to check empty files
        elif len(file_sizes[file_size]) > 1 and file_size == 0:
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

    # The only compulsory argument is the directory to search
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
