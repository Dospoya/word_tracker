from src.app.models.profile import EnglishLevel, EnglishVariant
from src.bot.keyboard.base import InlineKeyboardBase, InlineKeyboardPagination
from src.bot.constants.text import REGISTER_TEXT

REGISTER_CALLBACK = InlineKeyboardBase()._slugify(REGISTER_TEXT)


def registration_kb() -> InlineKeyboardBase:
    return InlineKeyboardBase(buttons=[REGISTER_TEXT])


async def registration_level_keyboard(
    page: int = 0,
) -> InlineKeyboardPagination:
    buttons: list[tuple[str, str]] = []
    buttons = [(level, f'level:{level.value}') for level in EnglishLevel]
    return InlineKeyboardPagination(
        buttons=buttons,
        columns=2,
        page_size=6,
        include_service_buttons=False,
        current_page=page,
    )


async def registration_variant_keyboard(
    page: int = 0,
) -> InlineKeyboardPagination:
    buttons: list[tuple[str, str]] = []
    buttons = [(variant, f'variant:{variant.value}') for variant in EnglishVariant]
    return InlineKeyboardPagination(
        buttons=buttons,
        columns=2,
        page_size=3,
        include_service_buttons=False,
        current_page=page,
    )
