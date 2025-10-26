from typing import cast

from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext

from bot.constants.text import WELCOME_REGISTRED_MESSAGE
from bot.fsm.user import UserMain
from bot.keyboard.inline.user import user_main_kb

service_router = Router()


@service_router.callback_query(F.data == "main_menu")
async def handle_main_menu(callback: types.CallbackQuery, state: FSMContext):
    callback_message = cast(types.Message, callback.message)
    await state.set_state(UserMain.main_menu)
    _ = await callback_message.edit_text(
        text=WELCOME_REGISTRED_MESSAGE, reply_markup=user_main_kb().build()
    )
    _ = await callback.answer()


async def handle_back(): ...
