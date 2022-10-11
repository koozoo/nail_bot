import logging
from aiogram import Bot, Dispatcher, executor, types
from config import TOKEN, db


logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):

    await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram.")


@dp.message_handler(commands=['buy'])
async def echo(message: types.Message):

    # old style:

    # await bot.send_message(message.chat.id, message.text)

    await message.answer('Покупка курса')


def main():
    executor.start_polling(dp, skip_updates=True)
