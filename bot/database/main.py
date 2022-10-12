import sqlite3


class DB:
    __instance = None

    def __init__(self):
        if not DB.__instance:
            print(" __init__ method called..")
        else:
            print("Instance already created:", self.get_instance())

    @classmethod
    def get_instance(cls):
        if not cls.__instance:
            cls.__instance = DB()
        return cls.__instance


class InitDataBase(DB):
    def __init__(self, name_db):
        super(DB, self).__init__()
        self.name_db = name_db

    def connect_db(self):
        con = sqlite3.connect(self.name_db)
        cursor = con.cursor()
        return con, cursor
