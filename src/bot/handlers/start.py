from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import (
    Message,
    ReplyKeyboardRemove
)
from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from sqlalchemy.ext.asyncio import AsyncSession

from src.bot.keyboard.base import InlineKeyboardBase
from src.bot.keyboard.inline.registration import (
    REGISTER_CALLBACK,
    registration_kb,
)
from src.bot.constants.text import (
    WELCOME_REGISTRATION_MESSAGE,
)
# from src.crud.user import user_crud
# from bot.keyboard.registration import (
#     get_language_level_keyboard,
#     get_language_variant_keyboard,
# )
# from bot.keyboard.keyboard import (
#     main_menu,
# )



start_router = Router()


async def start_handler(message: Message, state: FSMContext):
    tg_user_id = message.from_user.id
    # role = await get_user_role(tg_user_id)
    # match role:
    #     case 'user':
    #         ...
    #     case 'admin':
    #         ...
    #     case 'applicant':
    #         ...
    kb: InlineKeyboardBase = registration_kb().build()
    await message.answer(
        text=WELCOME_REGISTRATION_MESSAGE,
        reply_markup=kb,
    )
