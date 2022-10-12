from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


mainMenu = InlineKeyboardMarkup(row_width=3)

btnPrice = InlineKeyboardButton(text='Цены', callback_data='btnPrice')
btnAdd = InlineKeyboardButton(text='Записаться', callback_data='addEvent')
btnUpdate = InlineKeyboardButton(text='Перенсти запись', callback_data='updateEvent')
btnDel = InlineKeyboardButton(text='Отмена записи', callback_data='delEvent')

mainMenu.insert(btnAdd)
mainMenu.insert(btnUpdate)
mainMenu.insert(btnDel)
mainMenu.insert(btnPrice)


subMenuPrice = InlineKeyboardMarkup(row_width=1)

btnSubAdd = InlineKeyboardButton(text='Записаться', callback_data='addEvent')
btnBack = InlineKeyboardButton(text='Назад', callback_data='btnBack')

subMenuPrice.insert(btnSubAdd)
subMenuPrice.insert(btnBack)


priceMenu = InlineKeyboardMarkup(row_width=1)




