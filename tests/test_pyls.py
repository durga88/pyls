# tests/test_pyls.py
import pytest
from pyls import pyls, human_readable_size, find_item_by_path

def test_human_readable_size():
    assert human_readable_size(1023) == "1023.0B"
    assert human_readable_size(1024) == "1.0K"

def test_find_item_by_path():
    directory_structure = {
        "name": "root",
        "contents": [
            {
                "name": "file.txt",
                "size": 1234,
                "time_modified": 1699950453,
                "permissions": "-rw-r--r--"
            },
            {
                "name": "folder",
                "contents": [
                    {
                        "name": "subfile.txt",
                        "size": 5678,
                        "time_modified": 1699950454,
                        "permissions": "-rw-r--r--"
                    }
                ]
            }
        ]
    }
    assert find_item_by_path(directory_structure, ["folder", "subfile.txt"]) is not None
    assert find_item_by_path(directory_structure, ["non_existent"]) is None
