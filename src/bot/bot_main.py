import logging

from aiogram import Bot, Dispatcher
from aiogram.client import default
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from app.core.config import settings
from bot.routers.main import main_router
from bot.utils.utils import set_commands

TOKEN = settings.bot_token

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN, default=default.DefaultBotProperties(parse_mode=ParseMode.HTML))
storage = MemoryStorage()
dp = Dispatcher(storage=storage)
_ = dp.include_router(main_router)


async def main() -> None:
    await set_commands(bot)
    try:
        logging.info("Запуск бота...")
        await dp.start_polling(bot)
    finally:
        await bot.session.close()
