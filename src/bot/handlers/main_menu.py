# from aiogram import Router
# from aiogram.types import CallbackQuery
# from aiogram import F

# from src.bot.keyboard.keyboard import get_word_keyboard

# router = Router()

# MAIN_MENU = {
#     'word': ('Мой словарь', get_word_keyboard()),
#     'repeat': ('Тренировка', ...),
#     'help': ('Справка по работе с ботом', ...)
# }

# @router.callback_query(F.data.startswith('menu:'))
# async def main_handler(call: CallbackQuery):
#     message = call.message
#     if not message:
#         await call.answer('Не удалось обновить сообщение:', show_alert=True)
#         return
#     _, action = call.data.split(':')
#     text, keyboard = MAIN_MENU.get(action, (None, None))
#     if not text:
#         await call.answer('Неизвестная команда', show_alert=True)
#     await message.edit_text(text, reply_markup=keyboard)
#     await call.answer()
