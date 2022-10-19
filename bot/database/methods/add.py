from bot.database.main import InitDataBase


class InsertDataBase(InitDataBase):

    def add_data_step1(self, value: list):
        con, cursor = self.connect_db()
        cursor.execute(f"INSERT INTO contacts (telegram_id, telegram_name, last_order) VALUES(?,?,?)", value)

        con.commit()
        con.close()

    def add_all_product(self, value: list):
        con, cursor = self.connect_db()
        cursor.execute(f"INSERT INTO products (title, price) VALUES(?,?)", value)

        con.commit()
        con.close()


