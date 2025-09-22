from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from src.bot.keyboard.base import InlineKeyboardBase
from src.bot.keyboard.inline.registration import (
    registration_kb,
)
from src.bot.keyboard.inline.user import (
    user_main_kb,
)
from src.bot.constants.text import (
    WELCOME_REGISTRATION_MESSAGE,
)
from src.bot.serviсes.api import check_user_role


start_router = Router()


async def start_handler(message: Message, state: FSMContext):
    tg_id = message.from_user.id
    role = await check_user_role(tg_id)
    match role:
        case 'user':
            kb: InlineKeyboardBase = user_main_kb().build()
            await message.answer(
                text='Привет, пользователь!',
                reply_markup=kb,
            )
        case 'admin':
            await message.answer(text='Привет, админ!')
        case _:
            kb: InlineKeyboardBase = registration_kb().build()
            await message.answer(
                text=WELCOME_REGISTRATION_MESSAGE,
                reply_markup=kb,
            )
