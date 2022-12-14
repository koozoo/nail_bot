from aiogram.utils import executor
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from bot.filters import register_all_filters
from bot.handlers import register_all_handlers
from bot.database.models import register_models
from bot.handlers.user.main import send_message
import logging


from bot.misc.config import TOKEN

logging.basicConfig(level=logging.INFO)


async def __on_start_up(dp: Dispatcher) -> None:
    register_all_filters(dp)
    register_all_handlers(dp)
    register_models()


def start_bot():
    bot = Bot(token=TOKEN, parse_mode='HTML')
    dp = Dispatcher(bot, storage=MemoryStorage())
    executor.start_polling(dp, skip_updates=True, on_startup=__on_start_up)
