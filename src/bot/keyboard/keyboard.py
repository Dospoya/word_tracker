# from aiogram.types import (
#     InlineKeyboardButton,
#     InlineKeyboardMarkup,
#     KeyboardButton,
#     ReplyKeyboardMarkup
# )
# from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

# def main_menu():
#     kb = InlineKeyboardBuilder()
#     kb.button(text='Мой словарь', callback_data='menu:word')
#     kb.button(text='Тренировка', callback_data='menu:repeat')
#     kb.button(text='Как работать с ботом', callback_data='menu:help')
#     kb.adjust(1)
#     return kb.as_markup()

# def get_word_keyboard() -> InlineKeyboardMarkup:
#     kb = InlineKeyboardBuilder()
#     kb.button(text='Добавить новое слово', callback_data='word:add')
#     kb.button(text='Удалить слово', callback_data='word:remove')
#     kb.button(text='Показать все слова', callback_data='word:show')
#     kb.button(text='Скачать список слов', callback_data='word:download')
#     kb.adjust(1)
#     return kb.as_markup()

# def get_repeat_keyboard(word: str) -> InlineKeyboardMarkup:
#     return InlineKeyboardMarkup(
#         inline_keyboard=[
#             [
#                 InlineKeyboardButton(text='Запомнил', callback_data=f'remember:{word}'),
#                 InlineKeyboardButton(text='Пропустить', callback_data=f'skip:{word}')
#             ]
#         ]
#     )
