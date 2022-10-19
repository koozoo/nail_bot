from bot.database.main import InitDataBase


class CreateTable(InitDataBase):
    def crete_tables(self):
        con, cursor = self.connect_db()
        cursor.execute(f'CREATE TABLE IF NOT EXISTS contacts('
                       'telegram_id INTEGER PRIMARY KEY,'
                       'fullname VARCHAR(100),'
                       'telegram_name VARCHAR(100),'
                       'phone VARCHAR(15),'
                       'last_order VARCHAR(20)'
                       ')')
        con.commit()

        cursor.execute(f'CREATE TABLE IF NOT EXISTS orders('
                       'id INTEGER PRIMARY KEY AUTOINCREMENT,'
                       'date VARCHAR(100) NOT NULL,'
                       'contact_id INTEGER,'
                       'FOREIGN KEY(contact_id) REFERENCES contacts(contacts_id) ON DELETE CASCADE'
                       ')')
        con.commit()

        cursor.execute(f'CREATE TABLE IF NOT EXISTS products('
                       'dates_id INTEGER PRIMARY KEY AUTOINCREMENT,'
                       'title VARCHAR(100) NOT NULL,'
                       'price INTEGER'
                       ')')
        con.commit()

        con.close()

