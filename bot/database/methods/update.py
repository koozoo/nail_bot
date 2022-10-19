from bot.database.main import InitDataBase


class UpdateDataBase(InitDataBase):

    def update_name(self, id,  name):
        con, cursor = self.connect_db()
        cursor.execute(f"UPDATE contacts SET fullname='{name}' WHERE telegram_id={id} ")

        con.commit()
        con.close()

    def update_phone(self, id: int,  phone: str):
        con, cursor = self.connect_db()
        cursor.execute(f"UPDATE contacts SET  phone='{phone}' WHERE telegram_id={id}")

        con.commit()
        con.close()

    def update_step1(self, id: int,  value: list):
        con, cursor = self.connect_db()
        cursor.execute(f"UPDATE contacts SET  telegram_name='{value[0]}', last_order='{value[1]}' WHERE telegram_id={id}")

        con.commit()
        con.close()
