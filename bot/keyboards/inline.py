from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from bot.misc.GoogleSheets import GoogleSheet

gs = GoogleSheet()

mainMenu = InlineKeyboardMarkup(row_width=3)

btnPrice = InlineKeyboardButton(text='Цены', callback_data='btnPrice')
btnAdd = InlineKeyboardButton(text='Записаться', callback_data='addEventWeek')
btnUpdate = InlineKeyboardButton(text='Перенсти запись', callback_data='updateEvent')
btnDel = InlineKeyboardButton(text='Отмена записи', callback_data='delEvent')

mainMenu.insert(btnAdd)
mainMenu.insert(btnUpdate)
mainMenu.insert(btnDel)
mainMenu.insert(btnPrice)


subMenuPrice = InlineKeyboardMarkup(row_width=1)

btnSubAdd = InlineKeyboardButton(text='Записаться', callback_data='addEventWeek')
btnBack = InlineKeyboardButton(text='❌ Назад', callback_data='btnBack')

subMenuPrice.insert(btnSubAdd)
subMenuPrice.insert(btnBack)


priceMenu = InlineKeyboardMarkup(row_width=1)


date = gs.get_week_date()


weekMenu = InlineKeyboardMarkup(row_width=1)

btnWeek1 = InlineKeyboardButton(text=date[0], callback_data='week1')
btnWeek2 = InlineKeyboardButton(text=date[1], callback_data='week2')
btnWeek3 = InlineKeyboardButton(text=date[2], callback_data='week3')
btnWeek4 = InlineKeyboardButton(text=date[3], callback_data='week4')
btnWeek5 = InlineKeyboardButton(text=date[4], callback_data='week5')

weekMenu.insert(btnWeek1)
weekMenu.insert(btnWeek2)
weekMenu.insert(btnWeek3)
weekMenu.insert(btnWeek4)
weekMenu.insert(btnWeek5)

