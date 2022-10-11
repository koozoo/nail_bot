import logging
from aiogram import Bot, Dispatcher, executor, types
from config import TOKEN, db
import markups as nav
from GoogleSheets import test

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    user_name = message.from_user.full_name
    await bot.send_message(message.from_user.id, f'Привет, {user_name}', reply_markup=nav.mainMenu)


@dp.callback_query_handler(text='btnPrice')
async def print_price(message: types.message):
    await bot.delete_message(message.from_user.id, message.message.message_id)
    await bot.send_message(message.from_user.id, 'sdfsdfsdfsdf', reply_markup=nav.mainMenu)


def main():
    # executor.start_polling(dp, skip_updates=True)
    test()
