from aiogram import Dispatcher, types
from aiogram.types import Message
import bot.keyboards.inline as nav
from bot.misc.GoogleSheets import GoogleSheet
from bot.misc.util import print_data

gs = GoogleSheet()


async def start(msg: Message):
    user_name = msg.from_user.first_name
    text = f'Привет, {user_name}'

    # обновляем дату на сегодняшнюю, со смещением всех заказов
    gs.update_date_in_sheets()

    await msg.bot.send_message(msg.from_user.id, text, reply_markup=nav.mainMenu)


async def back(msg: Message):
    user_name = msg.from_user.first_name
    await msg.bot.delete_message(msg.from_user.id, msg.message.message_id)
    await msg.bot.send_message(msg.from_user.id, f'{user_name}, желаете записаться ?', reply_markup=nav.mainMenu)


async def watch_price(msg: types.Message):
    # get price data -> 'p_data'
    gs = GoogleSheet()
    price_range, dimension = 'прайс!B2:C32', 'ROWS'
    p_data = gs.get_data_sheets(price_range, dimension)

    await msg.bot.delete_message(msg.from_user.id, msg.message.message_id)
    await msg.bot.send_message(msg.from_user.id, print_data(p_data), reply_markup=nav.subMenuPrice)


def register_user_handlers(dp: Dispatcher):
    # todo: register all user handlers
    dp.register_message_handler(start, commands=['start', 'main'])
    dp.register_callback_query_handler(watch_price, text='btnPrice')
    dp.register_callback_query_handler(back, text='btnBack')




