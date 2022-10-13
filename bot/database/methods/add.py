from bot.database.main import InitDataBase


class InsertDataBase(InitDataBase):
    def __init__(self):
        super(InitDataBase).__init__(self.name_db)

    def add_data(self, data):
        con, cursor = self.connect_db()
        cursor.execute('INSERT INTO contacts VALUES(?,?,?)', data)
        con.commit()
        con.close()

