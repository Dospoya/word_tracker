from bot.constants.text import REGISTER_TEXT
from bot.keyboard.base import InlineBtn, InlineKeyboardBase, InlineKeyboardPagination
from contracts.shared.contracts import EnglishLevel, EnglishVariant

REGISTER_CALLBACK = InlineKeyboardBase()._slugify(REGISTER_TEXT)


def registration_kb() -> InlineKeyboardBase:
    return InlineKeyboardBase(buttons=[REGISTER_TEXT])


def registration_level_keyboard(
    page: int = 0,
) -> InlineKeyboardPagination:
    buttons: list[InlineBtn] = []
    buttons = [(level, f"level:{level.value}") for level in EnglishLevel]
    return InlineKeyboardPagination(
        buttons=buttons,
        columns=2,
        page_size=6,
        include_service_buttons=False,
        current_page=page,
    )


def registration_variant_keyboard(
    page: int = 0,
) -> InlineKeyboardPagination:
    buttons: list[InlineBtn] = []
    buttons = [(variant, f"variant:{variant.value}") for variant in EnglishVariant]
    return InlineKeyboardPagination(
        buttons=buttons,
        columns=2,
        page_size=3,
        include_service_buttons=False,
        current_page=page,
    )
