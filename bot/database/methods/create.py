from bot.database.main import InitDataBase


class CreateTable(InitDataBase):
    def crete_tables(self):
        con, cursor = self.connect_db()
        cursor.execute(f'CREATE TABLE IF NOT EXISTS contacts('
                       'contacts_id INTEGER PRIMARY KEY,'
                       'fullname VARCHAR(100) NOT NULL,'
                       'phone VARCHAR(15)'
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

