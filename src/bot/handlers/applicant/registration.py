import logging
from typing import cast

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, ReplyKeyboardMarkup

from bot.constants.text import (
    INVALID_NAME_TEXT,
    MSG_ENTER_LEVEL,
    MSG_ENTER_NAME,
    MSG_ENTER_VARIANT,
    MSG_REGISTERED_SUCCESS,
)
from bot.fsm.register import RegistrationState
from bot.keyboard.inline.registration import (
    REGISTER_CALLBACK,
    registration_level_keyboard,
    registration_variant_keyboard,
)
from bot.keyboard.inline.user import user_main_kb
from bot.services.api import full_user_registration
from bot.utils.validators import is_valid_russian_name

registration_router = Router()


async def error_reply(
    message: Message,
    err_msg: str,
    msg: str,
    kb: ReplyKeyboardMarkup | None = None,
) -> Message | None:
    """Создает сообщение об ошибке."""
    if kb:
        _ = await message.answer(text=err_msg)
        _ = await message.answer(
            text=msg,
            reply_markup=kb,
        )
    else:
        _ = await message.answer(text=err_msg)
        _ = await message.answer(text=msg)


@registration_router.callback_query(F.data == REGISTER_CALLBACK)
async def registration_start(
    callback: CallbackQuery,
    state: FSMContext,
) -> None:
    if callback.message is None:
        _ = await callback.answer("Сообщение не найдено")
        return
    _ = await callback.message.answer(
        MSG_ENTER_NAME,
    )
    await state.set_state(RegistrationState.waiting_for_name)


@registration_router.message(RegistrationState.waiting_for_name)
async def process_name(message: Message, state: FSMContext) -> None:
    name = message.text
    if name and not is_valid_russian_name(name):
        _ = await error_reply(
            message=message,
            err_msg=INVALID_NAME_TEXT,
            msg=MSG_ENTER_NAME,
        )
        return
    _ = await state.update_data(name=name)
    kb = registration_level_keyboard()
    _ = await message.answer(MSG_ENTER_LEVEL, reply_markup=kb.build())
    await state.set_state(RegistrationState.waiting_for_level)


@registration_router.callback_query(
    RegistrationState.waiting_for_level, F.data.startswith("level:")
)
async def process_level(
    callback: CallbackQuery,
    state: FSMContext,
) -> None:
    callback_message = cast(Message, callback.message)
    if callback.data is None:
        return
    _, level = callback.data.split(":")
    _ = await state.update_data(level=level)
    kb = registration_variant_keyboard()
    _ = await callback_message.answer(MSG_ENTER_VARIANT, reply_markup=kb.build())
    await state.set_state(RegistrationState.waiting_for_variant)


@registration_router.callback_query(
    RegistrationState.waiting_for_variant, F.data.startswith("variant:")
)
async def process_variant(
    callback: CallbackQuery,
    state: FSMContext,
) -> None:
    callback_message = cast(Message, callback.message)
    if callback.data is None:
        return
    _, variant = callback.data.split(":")
    _ = await state.update_data(variant=variant)
    data: dict[str, str] = await state.get_data()
    try:
        _ = await full_user_registration(
            first_name=data.get("name", ""),
            tg_id=callback.from_user.id,
            level=data.get("level", ""),
            variant=data.get("variant", ""),
        )
        _ = await callback_message.answer(
            MSG_REGISTERED_SUCCESS, reply_markup=user_main_kb().build()
        )
    except Exception as e:
        logging.info(f"Ошибка {e}")
        _ = await callback_message.answer(
            "Ошибка регистрации. Обратитесь к администратору"
        )
    await state.clear()
