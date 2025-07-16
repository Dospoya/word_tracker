import logging

from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher
from aiogram.client import default
from aiogram.enums import ParseMode

from src.app.core.config import settings
from src.bot.utils.utils import set_commands
from src.bot.routers.main import main_router
TOKEN=settings.bot_token

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN, default=default.DefaultBotProperties(parse_mode=ParseMode.HTML))
storage = MemoryStorage()
dp = Dispatcher(storage=storage)
dp.include_router(main_router)


async def main() -> None:
    await set_commands(bot)
    try:
        logging.info('Запуск бота...')
        await dp.start_polling(bot)
    finally:
        await bot.session.close()
