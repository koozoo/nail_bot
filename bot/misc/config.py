from dotenv import load_dotenv
import os
from bot.database.methods.create import CreateTable


load_dotenv()

# private data
TOKEN = os.getenv('TOKEN')
spreadsheet_id = os.getenv('SPREADSHEET_ID')

# INIT DATA BASE
DB_NAME = 'main.db'
db = CreateTable(DB_NAME)
db.crete_tables()

# client data
MASTER_NAME = 'ИМЯ'

