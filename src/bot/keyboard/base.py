import re

from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)


from src.bot.constants.text import (
    BACK_TEXT,
    MAIN_MENU_TEXT,
    PAGINATION_LEFT_TEXT,
    PAGINATION_RIGHT_TEXT,
)


class BaseKeyboard:
    """Абстрактный базовый класс для создания клавиатур.

    Атрибуты:
        buttons (list): Кнопки, заданные как список строк или пар (текст,
        callback_data).
        columns (int): Количество столбцов в клавиатуре.
        include_service_buttons (bool): Включать ли кнопки "Назад" и "В меню".
    """

    BACK_TEXT = BACK_TEXT
    MAIN_MENU_TEXT = MAIN_MENU_TEXT

    def __init__(
        self,
        buttons: list[str] | list[tuple[str, str]] = None,
        columns: int = 2,
        include_service_buttons: bool = False,
    ) -> None:
        """Инициализирует базовые параметры клавиатуры.

        Args:
            buttons (list[str] | list[tuple[str, str]]):Список кнопок (строки
            или пары (текст, callback_data)).
            columns (int): Количество столбцов.
            include_service_buttons (bool):Добавлять ли кнопки "Назад"
            и "В меню".

        """
        self.buttons = buttons or []
        self.columns = columns
        self.include_service_buttons = include_service_buttons

    def _slugify(self, text: str) -> str:
        """Преобразует строку в безопасный идентификатор для callback_data.

        Args:
            text (str): Входной текст кнопки.

        Returns:
            str: Безопасный идентификатор.

        """
        slug = re.sub(r'\W+', '_', text.strip().lower())
        return slug.strip('_')


class InlineKeyboardBase(BaseKeyboard):
    """Класс для создания inline-клавиатур.

    Атрибуты:
        state_id (str): Уникальный идентификатор состояния клавиатуры.
        для поддержки перехода "Назад".
    """

    def __init__(
        self,
        buttons: list[str] | list[tuple[str, str]] = None,
        columns: int = 2,
        include_service_buttons: bool = False,
    ) -> None:
        """Инициализирует inline-клавиатуру."""
        super().__init__(
            buttons=buttons,
            columns=columns,
            include_service_buttons=include_service_buttons,
        )
        self.state_id = self.generate_state_id()

    def generate_state_id(self) -> str:
        """Генерирует уникальный идентификатор состояния клавиатуры.

        Returns:
            str: Уникальный идентификатор клавиатуры (state_id).

        """
        base = '_'.join(
            self._slugify(text)
            if isinstance(text, str)
            else self._slugify(text[1])
            for text in self.buttons
        )
        return base or 'root'

    def _add_service_buttons(
        self,
        keyboard: list[list[InlineKeyboardButton]],
    ) -> None:
        """Добавляет сервисные кнопки в keyboard, если включены."""
        if self.include_service_buttons:
            service_row = []
            service_row.append(
                InlineKeyboardButton(
                    text=self.BACK_TEXT,
                    callback_data='back',
                ),
            )
            service_row.append(
                InlineKeyboardButton(
                    text=self.MAIN_MENU_TEXT,
                    callback_data='main_menu',
                ),
            )
            keyboard.append(service_row)

    def build(self) -> InlineKeyboardMarkup:
        """Строит объект InlineKeyboardMarkup из кнопок.

        Returns:
            InlineKeyboardMarkup: Собранная клавиатура.

        """
        keyboard = []
        row = []

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


class ReplyKeyboardBase(BaseKeyboard):
    """Класс для создания reply-клавиатур."""

    def build(self) -> ReplyKeyboardMarkup:
        """Строит объект ReplyKeyboardMarkup из кнопок.

        Returns:
            ReplyKeyboardMarkup: Собранная клавиатура.

        """
        keyboard = []
        row = []

        for button in self.buttons:
            if isinstance(button, str):
                btn = KeyboardButton(text=button)
            elif isinstance(button, dict):
                btn = KeyboardButton(**button)
            elif isinstance(button, (list, tuple)):
                # Позволяет задать текст и дополнительные параметры
                text, *params = button
                btn = KeyboardButton(
                    text=text, **(params[0] if params else {}),
                )
            else:
                raise ValueError(
                    f'Неподдерживаемый тип кнопки: {type(button)}',
                )

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
    """Inline-клавиатура с поддержкой пагинации.

    Атрибуты:
        page_size (int): Количество кнопок на странице.
        current_page (int): Текущая страница (0-индексация).
        total_pages (int): Общее количество страниц.
    """

    def __init__(
        self,
        buttons: list[str] | list[tuple[str, str]],
        columns: int = 2,
        page_size: int = 6,
        include_service_buttons: bool = False,
        current_page: int = 0,
    ) -> None:
        """Инициализирует пагинацию.

        Args:
            buttons (list[str | tuple[str, str]]): Все кнопки для пагинации.
            columns (int, optional): Количество столбцов на странице.
            page_size (int, optional): Количество кнопок на странице.
            include_service_buttons (bool, optional):Включать сервисные кнопки.
            current_page (int, optional):Номер текущей страницы (0-индексация).

        """
        super().__init__(buttons, columns, include_service_buttons)
        self.page_size = page_size
        self.current_page = current_page
        self.total_pages = (len(self.buttons) - 1) // self.page_size + 1

    def build(self) -> InlineKeyboardMarkup:
        """Строит inline-клавиатуру с кнопками текущей страницы и навигацией.

        Возвращает клавиатуру с кнопками только текущей страницы,
        кнопками навигации и сервисными кнопками.

        Returns:
            InlineKeyboardMarkup: Клавиатура с пагинацией.

        """
        keyboard = []

        start = self.current_page * self.page_size
        end = start + self.page_size
        page_buttons = self.buttons[start:end]

        row = []
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

        # Кнопки навигации
        if self.total_pages > 1:
            nav_row = []
            if self.current_page > 0:
                nav_row.append(
                    InlineKeyboardButton(
                        text=PAGINATION_LEFT_TEXT,
                        callback_data=f'page:{self.current_page - 1}',
                    ),
                )

            if self.current_page < self.total_pages - 1:
                nav_row.append(
                    InlineKeyboardButton(
                        text=PAGINATION_RIGHT_TEXT,
                        callback_data=f'page:{self.current_page + 1}',
                    ),
                )
            keyboard.append(nav_row)

        self._add_service_buttons(keyboard)

        return InlineKeyboardMarkup(inline_keyboard=keyboard)
