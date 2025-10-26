import re
from typing import ClassVar, Final, Generic, TypeVar, override

from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    KeyboardButtonPollType,
    KeyboardButtonRequestChat,
    KeyboardButtonRequestUser,
    ReplyKeyboardMarkup,
)
from pydantic import BaseModel, ConfigDict, Field

from bot.constants.text import (
    BACK_TEXT,
    MAIN_MENU_TEXT,
    PAGINATION_LEFT_TEXT,
    PAGINATION_RIGHT_TEXT,
)


class KBButtonType(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(extra="forbid")
    text: str
    request_chat: KeyboardButtonRequestChat | None = None
    request_contact: bool | None = None
    request_poll: KeyboardButtonPollType | None = None
    request_user: KeyboardButtonRequestUser | None = Field(
        None, json_schema_extra={"deprecated": True}
    )

    def to_dict(self) -> KeyboardButton:
        return KeyboardButton(
            text=self.text,
            request_contact=self.request_contact,
            request_poll=self.request_poll,
            request_user=self.request_user,
            request_chat=self.request_chat,
        )


InlineBtn = str | tuple[str, str]
ReplyBtn = str | KBButtonType

B = TypeVar("B")


class BaseKeyboard(Generic[B]):
    BACK_TEXT: Final[str] = BACK_TEXT
    MAIN_MENU_TEXT: Final[str] = MAIN_MENU_TEXT

    def __init__(
        self,
        buttons: list[B] | None = None,
        columns: int = 2,
        include_service_buttons: bool = False,
    ) -> None:
        self.buttons: list[B] = buttons or []
        self.columns: int = columns
        self.include_service_buttons: bool = include_service_buttons

    def _slugify(self, text: str) -> str:
        slug = re.sub(r"\W+", "_", text.strip().lower())
        return slug.strip("_")


class InlineKeyboardBase(BaseKeyboard[InlineBtn]):
    def __init__(
        self,
        buttons: list[InlineBtn] | None = None,
        columns: int = 2,
        include_service_buttons: bool = False,
    ) -> None:
        super().__init__(
            buttons=buttons,
            columns=columns,
            include_service_buttons=include_service_buttons,
        )
        self.state_id: str = self.generate_state_id()

    def generate_state_id(self) -> str:
        """Генерирует уникальный идентификатор состояния клавиатуры.

        Returns:
            str: Уникальный идентификатор клавиатуры (state_id).

        """
        base = "_".join(
            self._slugify(text) if isinstance(text, str) else self._slugify(text[1])
            for text in self.buttons
        )
        return base or "root"

    def _add_service_buttons(
        self,
        keyboard: list[list[InlineKeyboardButton]],
    ) -> None:
        if self.include_service_buttons:
            service_row: list[InlineKeyboardButton] = []
            service_row.append(
                InlineKeyboardButton(
                    text=self.BACK_TEXT,
                    callback_data="back",
                ),
            )
            service_row.append(
                InlineKeyboardButton(
                    text=self.MAIN_MENU_TEXT,
                    callback_data="main_menu",
                ),
            )
            keyboard.append(service_row)

    def build(self) -> InlineKeyboardMarkup:
        keyboard: list[list[InlineKeyboardButton]] = []
        row: list[InlineKeyboardButton] = []

        for button in self.buttons:
            if isinstance(button, tuple):
                text, callback_data = button
            else:
                text = button
                callback_data = self._slugify(text)

            row.append(
                InlineKeyboardButton(text=text, callback_data=callback_data),
            )

            if len(row) >= self.columns:
                keyboard.append(row)
                row = []

        if row:
            keyboard.append(row)
        self._add_service_buttons(keyboard)
        return InlineKeyboardMarkup(inline_keyboard=keyboard)


class ReplyKeyboardBase(BaseKeyboard[ReplyBtn]):
    def __init__(
        self,
        buttons: list[ReplyBtn],
        columns: int = 2,
        include_service_buttons: bool = False,
        one_time_keyboard: bool = False,
    ) -> None:
        super().__init__(buttons, columns, include_service_buttons)
        self.one_time_keyboard: Final[bool] = one_time_keyboard

    def build(self) -> ReplyKeyboardMarkup:
        keyboard: list[list[KeyboardButton]] = []
        row: list[KeyboardButton] = []

        for button in self.buttons:
            if isinstance(button, str):
                btn = KeyboardButton(text=button)
            else:
                btn = button.to_dict()

            row.append(btn)

            if len(row) >= self.columns:
                keyboard.append(row)
                row = []

        if row:
            keyboard.append(row)

        if self.include_service_buttons:
            service_row = [
                KeyboardButton(text=self.BACK_TEXT),
                KeyboardButton(text=self.MAIN_MENU_TEXT),
            ]
            keyboard.append(service_row)

        return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


class InlineKeyboardPagination(InlineKeyboardBase):
    def __init__(
        self,
        buttons: list[InlineBtn],
        columns: int = 2,
        page_size: int = 6,
        include_service_buttons: bool = False,
        current_page: int = 0,
    ) -> None:
        super().__init__(buttons, columns, include_service_buttons)
        self.page_size: int = page_size
        self.current_page: int = max(0, current_page)
        self.total_pages: int = (len(self.buttons) - 1) // self.page_size + 1

    @override
    def build(self) -> InlineKeyboardMarkup:
        keyboard: list[list[InlineKeyboardButton]] = []
        row: list[InlineKeyboardButton] = []

        start = self.current_page * self.page_size
        end = start + self.page_size
        page_buttons: list[InlineBtn] = self.buttons[start:end]

        for button in page_buttons:
            if isinstance(button, tuple):
                text, callback_data = button
            else:
                text = button
                callback_data = self._slugify(text)

            row.append(
                InlineKeyboardButton(text=text, callback_data=callback_data),
            )

            if len(row) >= self.columns:
                keyboard.append(row)
                row = []

        if row:
            keyboard.append(row)

        if self.total_pages > 1:
            nav_row: list[InlineKeyboardButton] = []
            if self.current_page > 0:
                nav_row.append(
                    InlineKeyboardButton(
                        text=PAGINATION_LEFT_TEXT,
                        callback_data=f"page:{self.current_page - 1}",
                    ),
                )

            if self.current_page < self.total_pages - 1:
                nav_row.append(
                    InlineKeyboardButton(
                        text=PAGINATION_RIGHT_TEXT,
                        callback_data=f"page:{self.current_page + 1}",
                    ),
                )
            keyboard.append(nav_row)

        self._add_service_buttons(keyboard)

        return InlineKeyboardMarkup(inline_keyboard=keyboard)
