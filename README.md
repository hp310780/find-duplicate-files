# FindDuplicateFiles

![FindDuplicateFiles](https://github.com/hp310780/FindDuplicateFiles/workflows/Python%20application/badge.svg)

A fast and efficient way to find duplicate files in a directory. Installable as a command line interface 
(please see Installing below).

This module will walk the given directory tree and then group files by size 
(indicating potential duplicate content) followed by comparing the hash of the file.
This hash can be chunked by passing in a chunk arg. This will compute an initial hash for a chunk of the file 
before then computing the full hash if the first hash matched, thus avoiding computing
expensive hashes on large files.

### Prerequisites

* Python 3.6.5

### Installing

```
> pip3 install find-duplicate-files
> find_duplicate_files --dir /path/to/dir --chunk 2
```
To run as a Python module:
```
import find_duplicate_files
# required arg: dir, optional: chunk
find_duplicate_files.find_duplicate_files("/path/to/dir", chunk=1)
```

## Running the tests

To run the tests, please use the following commands:

```
> cd <FindDuplicateFiles directory>
> pytest
```

## Test Data

The test data provided takes the following form - 
* tests/test_data/TestFindDuplicateFilesByHash: 5 .txt files of equal size (29 bytes). 1.txt and 3.txt are the same content. 4.txt and 5.txt are the same content. 2.txt is different contents (but the same size). Used to verify the find_duplicate_files.find_duplicate_files_by_hash function.
* tests/test_data/TestGenerateHash/1.txt: 1 .txt file with which to compare the outcome of find_duplicate_files.generate_hash to.

## Performance

An optional performance script to compare the performance of hashing the full file versus the chunked approach when finding duplicate files. Outputs performance metrics.
To run:
```
> cd <FindDuplicateFiles/metrics directory>
> python performance.py
```
Example output:
```
Method 1 - Generate full hash returns correct duplicates.Time 0.006515709001178038
Method 2 - Generate chunked hash returns correct duplicates.Time 0.006872908999866922
```

## Benchmarking
| Attempt | #1 | #2 | #3 | #4 |
| :---: | :---: | :---: | :---:| :---: |
| Chunk Size | 1 | 1 | 8 | 8 |
| Seconds | 5.4 | 4.16 | 3.25 | 3.27 |

Test Data: 10.9gb, 3653 files, 128 duplicates, largest file ~156mb

## Further Optimisations
* Investigate optimal chunk size given common file type
* Investigate threading for performance
* Investigate different hashing algorithms
* Investigate recursive chunking - i.e. Eliminating files that differ