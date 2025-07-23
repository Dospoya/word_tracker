from src.bot.keyboard.base import (
    InlineKeyboardBase,
    InlineKeyboardPagination
)
from src.bot.constants.text import (
    MAIN_MENU_OPTION_PROFILE,
    MAIN_MENU_OPTION_HELP,
    MAIN_MENU_OPTION_VOCABULARY,
    MAIN_MENU_OPTION_PRACTICE,
)


def user_main_kb() -> InlineKeyboardBase:
    buttons: list[tuple[str, str]] = [
        (MAIN_MENU_OPTION_VOCABULARY, 'vocabulary'),
        (MAIN_MENU_OPTION_PRACTICE, 'practice'),
        (MAIN_MENU_OPTION_PROFILE, 'profile'),
        (MAIN_MENU_OPTION_HELP, 'help'),
    ]
    return InlineKeyboardBase(
        buttons=buttons,
    )
