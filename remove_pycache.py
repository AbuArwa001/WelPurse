#!/usr/bin/env python3
import os
import shutil


def remove_pycache(root_dir):
    """Walk through the directory tree and remove __pycache__ directories."""
    for dirpath, dirnames, _ in os.walk(root_dir):
        if "__pycache__" in dirnames:
            pycache_path = os.path.join(dirpath, "__pycache__")
            print("Removing {}".format(pycache_path))
            shutil.rmtree(pycache_path)


if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.realpath(__file__))
    remove_pycache(current_dir)
