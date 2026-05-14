from typing import Any

from bot.constants.text import (
    ADD_WORD_TEXT,
    CONFIRM_TEXT,
    DECLINE_TEXT,
    DELETE_PROFILE_TEXT,
    DELETE_WORD_TEXT,
    DETAIL_WORD_TEXT,
    DOWNLOAD_WORDS_TEXT,
    EDIT_PROFILE_TEXT,
    MAIN_MENU_OPTION_HELP,
    MAIN_MENU_OPTION_PRACTICE,
    MAIN_MENU_OPTION_PROFILE,
    MAIN_MENU_OPTION_VOCABULARY,
    RETURN_TO_LIST_TEXT,
    SHOW_WORDS_TEXT,
)
from bot.keyboard.base import InlineBtn, InlineKeyboardBase, InlineKeyboardPagination


def user_main_kb() -> InlineKeyboardBase:
    buttons: list[InlineBtn] = [
        (MAIN_MENU_OPTION_VOCABULARY, "vocabulary"),
        (MAIN_MENU_OPTION_PRACTICE, "practice"),
        (MAIN_MENU_OPTION_PROFILE, "profile"),
        (MAIN_MENU_OPTION_HELP, "help"),
    ]
    return InlineKeyboardBase(
        buttons=buttons,
    )


def user_profile_kb() -> InlineKeyboardBase:
    buttons: list[InlineBtn] = [
        (EDIT_PROFILE_TEXT, "edit_profile"),
        (DELETE_PROFILE_TEXT, "delete_profile"),
    ]
    return InlineKeyboardBase(
        buttons=buttons,
        include_service_buttons=True,
    )


def user_voc_kb() -> InlineKeyboardBase:
    buttons: list[InlineBtn] = [
        (ADD_WORD_TEXT, "add_word"),
        (SHOW_WORDS_TEXT, "show_all_words"),
        (DOWNLOAD_WORDS_TEXT, "download_words"),
    ]
    return InlineKeyboardBase(
        buttons=buttons,
        include_service_buttons=True,
    )


def user_practice_kb():
    """Заглушка для практики.

    InlineKeyboardButton(text='Запомнил', callback_data=f'remember:{word}'),
    InlineKeyboardButton(text='Пропустить', callback_data=f'skip:{word}')
    """


def user_confirm_kb():
    buttons: list[InlineBtn] = [
        (CONFIRM_TEXT, "confirm"),
        (DECLINE_TEXT, "decline"),
    ]
    return InlineKeyboardBase(
        buttons=buttons,
    )


def user_records_kb(
    records: list[dict[str, Any]], page: int = 0
) -> InlineKeyboardPagination:
    word_buttons: list[InlineBtn] = []
    for record in records:
        word = record.get("global_word").get("word")
        word_id = record.get("id")
        if isinstance(word, str) and isinstance(word_id, int):
            word_buttons.append((word, f"word:select:{word_id}"))
    return InlineKeyboardPagination(
        buttons=word_buttons, current_page=page, namespace="word"
    )


def user_word_kb(word_id: int, page: int, sid: int):
    buttons: list[InlineBtn] = [
        (DETAIL_WORD_TEXT, f"word:detail:{word_id}:{page}:{sid}"),
        (RETURN_TO_LIST_TEXT, f"w:page:{page}:{sid}"),
        (DELETE_WORD_TEXT, f"word:delete:{word_id}:{page}:{sid}"),
    ]
    return InlineKeyboardBase(
        buttons=buttons,
    )
