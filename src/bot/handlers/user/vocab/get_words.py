from typing import cast

from aiogram import F, Router, types

from bot.keyboard.inline.user import user_records_kb
from bot.services.api import get_words_by_tg_id

list_router = Router(name="vocabulary_list")


@list_router.callback_query(F.data == "show_all_words")
async def show_all_words(callback_query: types.CallbackQuery):
    callback_message = cast(types.Message, callback_query.message)
    records = await get_words_by_tg_id(callback_query.from_user.id)
    if not records:
        _ = await callback_message.edit_text(
            "Добавьте первое слово ",
        )
        _ = await callback_query.answer()
    _ = await callback_message.edit_text(
        "Список добавленных слов 👇",
        reply_markup=user_records_kb(records).build(),
    )
    _ = await callback_query.answer()


@list_router.callback_query(F.data.startswith('word:'))
async def show_word()
