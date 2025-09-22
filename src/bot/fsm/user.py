from aiogram.fsm import State, StatesGroup


class UserState(StatesGroup):
    user_main = State()
