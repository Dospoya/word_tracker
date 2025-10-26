from aiogram import Router

from bot.handlers.user.vocab.add_word import add_router
from bot.handlers.user.vocab.get_words import list_router

vocabulary_router = Router(name="vocabulary")

_ = vocabulary_router.include_router(add_router)
_ = vocabulary_router.include_router(list_router)


__all__ = ["vocabulary_router"]
