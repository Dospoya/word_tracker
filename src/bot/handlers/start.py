from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, Message

from bot.constants.text import (
    WELCOME_REGISTRATION_MESSAGE,
)
from bot.fsm.user import UserMain
from bot.keyboard.inline.registration import (
    registration_kb,
)
from bot.keyboard.inline.user import (
    user_main_kb,
)
from bot.services.api import check_user_role


async def start_handler(message: Message, state: FSMContext):
    user = message.from_user
    if user is None:
        print("User is None")
        return
    tg_id = user.id
    role = await check_user_role(tg_id)
    match role:
        case "user":
            await state.set_state(UserMain.main_menu)
            user_kb: InlineKeyboardMarkup = user_main_kb().build()
            _ = await message.answer(
                text="Привет, пользователь!",
                reply_markup=user_kb,
            )
        case "admin":
            _ = await message.answer(text="Привет, админ!")
        case _:
            await state.clear()
            kb: InlineKeyboardMarkup = registration_kb().build()
            _ = await message.answer(
                text=WELCOME_REGISTRATION_MESSAGE,
                reply_markup=kb,
            )
