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

    def crete_tables(self):
        con, cursor = self.connect_db()
        cursor.execute(f'CREATE TABLE IF NOT EXISTS contacts('
                       'contacts_id INTEGER PRIMARY KEY AUTOINCREMENT,'
                       'fullname VARCHAR(100) NOT NULL,'
                       'phone VARCHAR(15) NOT NULL'
                       ')')
        con.commit()

        cursor.execute(f'CREATE TABLE IF NOT EXISTS dates('
                       'dates_id INTEGER PRIMARY KEY AUTOINCREMENT,'
                       'dates VARCHAR(100) NOT NULL,'
                       'contact_id INTEGER,'
                       'FOREIGN KEY(contact_id) REFERENCES contacts(contacts_id) ON DELETE CASCADE'
                       ')')
        con.commit()

        con.close()

    def add_contact(self, name, phone):
        pass

    def add_date(self, event):
        pass

