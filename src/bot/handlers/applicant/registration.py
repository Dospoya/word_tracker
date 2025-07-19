import logging

from aiogram.types import (
    CallbackQuery,
    Message,
    ReplyKeyboardMarkup
)
from aiogram import F, Router
from aiogram.fsm.context import FSMContext

from src.bot.constants.text import (
    INVALID_NAME_TEXT,
    MSG_ENTER_NAME,
    MSG_ENTER_LEVEL,
    MSG_ENTER_VARIANT,
    MSG_REGISTERED_SUCCESS
)
from src.bot.fsm.register import RegistrationState
from src.bot.keyboard.inline.registration import (
    REGISTER_CALLBACK,
    registration_level_keyboard,
    registration_variant_keyboard,
)
from src.bot.serviсes.api import full_user_registration
from src.bot.utils.validators import is_valid_russian_name
from distutils.log import info


registration_router = Router()


async def error_reply(
    message: Message,
    err_msg: str,
    msg: str,
    kb: ReplyKeyboardMarkup = None,
) -> Message:
    """Создает сообщение об ошибке."""
    if kb:
        await message.answer(text=err_msg)
        await message.answer(
            text=msg,
            reply_markup=kb,
        )
    else:
        await message.answer(text=err_msg)
        await message.answer(text=msg)


@registration_router.callback_query(F.data == REGISTER_CALLBACK)
async def registration_start(
    callback: CallbackQuery,
    state: FSMContext,
) -> None:
    await state.set_state(RegistrationState.waiting_for_name)
    await callback.message.answer(
        MSG_ENTER_NAME,
    )


@registration_router.message(RegistrationState.waiting_for_name)
async def process_name(message: Message, state: FSMContext) -> None:
    name = message.text
    if name and not is_valid_russian_name(name):
        await error_reply(
            message=message,
            err_msg=INVALID_NAME_TEXT,
            msg=MSG_ENTER_NAME,
        )
        return
    await state.update_data(name=name)
    kb = await registration_level_keyboard()
    await message.answer(
        MSG_ENTER_LEVEL,
        reply_markup=kb.build()
    )
    await state.set_state(RegistrationState.waiting_for_level)


@registration_router.callback_query(
    RegistrationState.waiting_for_level,
    F.data.startswith('level:')
)
async def process_level(
    callback: CallbackQuery,
    state: FSMContext,
) -> None:
    _, level = callback.data.split(':')
    await state.update_data(level=level)
    kb = await registration_variant_keyboard()
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.answer(
        MSG_ENTER_VARIANT,
        reply_markup=kb.build()
    )
    await state.set_state(RegistrationState.waiting_for_variant)


@registration_router.callback_query(
    RegistrationState.waiting_for_variant,
    F.data.startswith('variant:')
)
async def process_variant(
    callback: CallbackQuery,
    state: FSMContext,
) -> None:
    _, variant = callback.data.split(':')
    await state.update_data(variant=variant)
    await callback.message.edit_reply_markup(reply_markup=None)
    data = await state.get_data()
    print(data)
    try:
        await full_user_registration(
            first_name=data.get('name'),
            tg_id=callback.from_user.id,
            level=data.get('level'),
            variant=data.get('variant'),
        )
        await callback.message.answer(MSG_REGISTERED_SUCCESS)
    except Exception as e:
        logging.info(f'Ошибка {e}')
        await callback.message.answer('Ошибка регистрации. Обратитесь к администратору')
    await state.clear()
    return
