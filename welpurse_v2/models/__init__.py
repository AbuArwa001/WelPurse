#!/usr/bin/python3
"""
initialize the models package
"""

from os import getenv


storage_t = getenv("STORAGE_TYPE")

if storage_t == "db":
    from welpurse_v2.models.engine.db_storage import DBStorage

    storage = DBStorage()
else:
    from welpurse_v2.models.engine.file_storage import FileStorage

    storage = FileStorage()
storage.reload()
