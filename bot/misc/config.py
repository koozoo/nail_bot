from dotenv import load_dotenv
import os
from bot.database.db import InitDataBase


load_dotenv()

# private data
TOKEN = os.getenv('TOKEN')
spreadsheet_id = os.getenv('SPREADSHEET_ID')

# INIT DATA BASE
DB_NAME = 'main.db'
db = InitDataBase(DB_NAME)
db.crete_tables()

