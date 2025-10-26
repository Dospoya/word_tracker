import logging
from typing import cast

from aiogram import Bot, F, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.utils.chat_action import ChatActionSender

from bot.fsm.user import UserMain, VocabAdd
from bot.keyboard.inline.user import user_confirm_kb, user_voc_kb
from bot.services.api import add_word, get_word
from bot.services.converter import Entry, format_entry

add_router = Router(name="vocabulary_add")


@add_router.callback_query(F.data == "vocabulary", UserMain.main_menu)
async def start_vocabulary(callback: types.CallbackQuery):
    bot = cast(Bot, callback.bot)
    callback_message = cast(types.Message, callback.message)
    async with ChatActionSender.typing(bot=bot, chat_id=callback.from_user.id):
        try:
            _ = await callback_message.edit_text(
                "Добро пожаловать в словарь! Ознакомьтесь с доступными командами:",
                reply_markup=user_voc_kb().build(),
            )
        except Exception:
            _ = await callback_message.answer(
                "Добро пожаловать в словарь! Ознакомьтесь с доступными командами:",
                reply_markup=user_voc_kb().build(),
            )
    _ = await callback.answer()


@add_router.callback_query(F.data == "add_word")
async def adding_word(callback: types.CallbackQuery, state: FSMContext):
    _ = await callback.answer()
    _ = await state.set_state(VocabAdd.waiting_for_word)
    if callback.message is None:
        return
    _ = await callback.message.answer("Введите слово:")


@add_router.message(VocabAdd.waiting_for_word, F.text)
async def handle_word_input(message: types.Message, state: FSMContext):
    if message.text is None:
        return
    word = message.text.strip()
    unformatted_word: Entry | None = await get_word(word)
    short_example = format_entry(unformatted_word, short_definition=True)
    if short_example is None:
        _ = await message.answer("Слово не найдено. Проверьте правильность написания.")
        return
    _ = await state.update_data(word=word)
    _ = await message.answer(short_example, reply_markup=user_confirm_kb().build())
    _ = await state.set_state(VocabAdd.waiting_for_confirm)


@add_router.callback_query(VocabAdd.waiting_for_confirm, F.data == "decline")
async def handle_decline_input(callback: types.CallbackQuery, state: FSMContext):
    callback_message = cast(types.Message, callback.message)
    _ = await callback.answer(
        "Операция отменена. Возвращаемся в меню словаря",
    )
    _ = await callback_message.edit_text(
        "Меню словаря:", reply_markup=user_voc_kb().build()
    )
    _ = await state.clear()


@add_router.callback_query(VocabAdd.waiting_for_confirm, F.data == "confirm")
async def handle_confirm_input(callback: types.CallbackQuery, state: FSMContext):
    callback_message = cast(types.Message, callback.message)
    data: dict[str, str] = await state.get_data()
    try:
        result = await add_word(word=data["word"], tg_id=callback.from_user.id)
        if result and result.get("created"):
            _ = await callback_message.edit_text(
                "Слово успешно добавлено в словарь",
                reply_markup=user_voc_kb().build(),
            )
        else:
            _ = await callback_message.edit_text(
                "Слово уже добавлено в ваш словарь",
                reply_markup=user_voc_kb().build(),
            )
    except Exception as e:
        logging.info(f"Ошибка {e}")
        _ = await callback_message.answer(
            "Ошибка добавления слова. Обратитесь к администратору"
        )
    _ = await state.clear()
