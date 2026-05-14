from typing import cast

from aiogram import F, Router, types

from bot.keyboard.inline.user import user_records_kb, user_word_kb
from bot.services.api import get_words_by_tg_id
from bot.services.converter import format_entry

list_router = Router(name="vocabulary_list")


def _extract_suffix(data: str, prefix: str) -> str | None:
    if not data.startswith(prefix):
        return None
    return data.removeprefix(prefix)


def _parse_word_id(data: str) -> int | None:
    for prefix in ("word:select:", "word:detail:", "word:delete:"):
        suffix = _extract_suffix(data, prefix)
        if suffix is None:
            continue
        word_id = suffix.split(":")[0]
        if word_id.isdigit():
            return int(word_id)
    return None


@list_router.callback_query(F.data == "show_all_words")
async def show_all_words(callback_query: types.CallbackQuery):
    callback_message = cast(types.Message, callback_query.message)
    records = await get_words_by_tg_id(callback_query.from_user.id)
    if not records:
        _ = await callback_message.edit_text(
            "Добавьте первое слово ",
        )
        _ = await callback_query.answer()
        return
    _ = await callback_message.edit_text(
        "Список добавленных слов 👇\n Страница 1",
        reply_markup=user_records_kb(records, page=0).build(),
    )
    _ = await callback_query.answer()


@list_router.callback_query(F.data.startswith("word:select:"))
async def show_word(callback_query: types.CallbackQuery):
    callback_message = cast(types.Message, callback_query.message)
    data = callback_query.data or ""
    word_id = _parse_word_id(data)
    if word_id is None:
        _ = await callback_query.answer(
            "Некорректный идентификатор слова",
            show_alert=True,
        )
        return

    records = await get_words_by_tg_id(callback_query.from_user.id)
    selected = next((record for record in records if record.get("id") == word_id), None)
    if selected is None:
        _ = await callback_query.answer("Слово не найдено", show_alert=True)
        return

    page = next(
        (index for index, record in enumerate(records) if record.get("id") == word_id),
        0,
    ) // 6
    state_id = user_records_kb(records, page=page).state_id
    entry = selected.get("global_word")
    text = format_entry(entry if isinstance(entry, dict) else None)
    if text is None:
        text = "Не удалось отобразить карточку слова."
    _ = await callback_message.edit_text(
        text,
        reply_markup=user_word_kb(word_id, page, state_id).build(),
    )
    _ = await callback_query.answer()


@list_router.callback_query(F.data.startswith("w:page:"))
async def return_to_words_page(callback_query: types.CallbackQuery):
    callback_message = cast(types.Message, callback_query.message)
    data = callback_query.data or ""
    parts = data.split(":")
    if len(parts) != 4 or not parts[2].isdigit():
        _ = await callback_query.answer(
            "Не удалось открыть список слов",
            show_alert=True,
        )
        return

    page = max(int(parts[2]) - 1, 0)
    records = await get_words_by_tg_id(callback_query.from_user.id)
    if not records:
        _ = await callback_message.edit_text("Добавьте первое слово")
        _ = await callback_query.answer()
        return

    _ = await callback_message.edit_text(
        f"Список добавленных слов 👇\n Страница {page + 1}",
        reply_markup=user_records_kb(records, page=page).build(),
    )
    _ = await callback_query.answer()


@list_router.callback_query(F.data.startswith("word:detail:"))
async def show_word_detail(callback_query: types.CallbackQuery):
    _ = await show_word(callback_query)


@list_router.callback_query(F.data.startswith("word:delete:"))
async def delete_word_stub(callback_query: types.CallbackQuery):
    _ = await callback_query.answer(
        "Удаление слова пока не реализовано",
        show_alert=True,
    )
