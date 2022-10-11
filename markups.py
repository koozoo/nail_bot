from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


mainMenu = InlineKeyboardMarkup(row_width=3)
btnPrice = InlineKeyboardButton(text='Цены', callback_data='btnPrice')
btnAdd = InlineKeyboardButton(text='Записаться', url='https://t.me/+2ma0p9Q84ppjNjQy')
btnUpdate = InlineKeyboardButton(text='Перенсти запись', url='https://t.me/+2ma0p9Q84ppjNjQy')
btnDel = InlineKeyboardButton(text='Отмена записи', url='https://t.me/+2ma0p9Q84ppjNjQy')

mainMenu.insert(btnAdd)
mainMenu.insert(btnUpdate)
mainMenu.insert(btnDel)
mainMenu.insert(btnPrice)
