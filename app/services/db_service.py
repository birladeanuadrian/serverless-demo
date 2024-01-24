import os
from contextlib import contextmanager
from typing import ContextManager

import pymongo
from pymongo.database import Database


class DbService:
    @contextmanager
    def get_database(self) -> ContextManager[Database]:
        conn = None
        try:
            conn = pymongo.MongoClient(os.getenv("MONGO_URI"))
            yield conn.get_database("technical-screen")
        finally:
            if conn:
                conn.close()
