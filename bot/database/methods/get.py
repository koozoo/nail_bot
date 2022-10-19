from bot.database.main import InitDataBase


class GetDataBase(InitDataBase):

    def get_data_where_id(self, id):
        con, cursor = self.connect_db()
        data = cursor.execute(f"SELECT * FROM contacts WHERE telegram_id={id}").fetchall()
        con.close()
        return data