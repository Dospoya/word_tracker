from src.bot.keyboard.base import InlineKeyboardBase, InlineKeyboardPagination
from src.bot.constants.text import REGISTER_TEXT

REGISTER_CALLBACK = InlineKeyboardBase()._slugify(REGISTER_TEXT)


async def user_main_kb():
    ...
