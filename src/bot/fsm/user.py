from aiogram.fsm.state import State, StatesGroup


class UserMain(StatesGroup):
    main_menu = State()


class VocabAdd(StatesGroup):
    waiting_for_word = State()
    waiting_for_confirm = State()


class VocabDelete(StatesGroup):
    delete_word = State()
    confirm = State()
