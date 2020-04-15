import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
     name='find-duplicate-files',
     version='2.1.0',
     scripts=['find_duplicate_files'],
     author="hp310780",
     description="Module to find duplicate files in a directory",
     long_description=long_description,
     long_description_content_type='text/markdown',
     url="https://github.com/hp310780/FindDuplicateFiles",
     py_modules=['find_duplicate_files'],
     license='MIT License',
     classifiers=[
         "Programming Language :: Python :: 3"
     ],

 )