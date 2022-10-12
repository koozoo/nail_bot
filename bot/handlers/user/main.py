from aiogram import Dispatcher
from aiogram.types import Message
import bot.keyboards.inline as nav


async def start(msg: Message):
    user_name = msg.from_user.first_name
    await msg.bot.send_message(msg.from_user.id, f'Привет, {user_name}', reply_markup=nav.mainMenu)


async def print_price(msg: Message):
    await msg.bot.delete_message(msg.from_user.id, msg.message_id)
    await msg.bot.send_message(msg.from_user.id, 'sdfsdfsdfsdf', reply_markup=nav.mainMenu)


def register_user_handlers(dp: Dispatcher):
    # todo: register all user handlers
    dp.register_message_handler(start, commands=['start'])
    dp.register_callback_query_handler(print_price, text='btnPrice')




