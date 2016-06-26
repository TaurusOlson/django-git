"""
Find the README of a Git project and convert it to HTML if it's possible
"""

from pathlib import Path


def find_readme(directory):
    """Return the path of the README contained in the given directory

    :directory: The directory
    :returns: filter object

    """
    dir_content = Path(directory).expanduser().iterdir()
    return filter(lambda x: x.name.upper().startswith("README"), dir_content)


files = list(find_readme("~/Dropbox/Projects/fntools"))

if len(files) == 1:
    with files[0].open() as f:
        print(f.read())
