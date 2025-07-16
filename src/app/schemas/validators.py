from re import match
from string import ascii_letters

ENGLISH_WORD_PATTERN = rf'^{ascii_letters}+(-{ascii_letters}+)*$'
RUSSIAN_WORD_PATTERN = r'^[а-яё]+(-[а-яё]+)*$'

NON_EMPTY = 'Поле не может быть пустым.'
ENGLISH_WORD_ERROR = (
    'Слово должно состоять только из букв английского алфавита '
    'и может содержать дефисы.'
)
RUSSIAN_WORD_ERROR = (
    'Слово должно состоять только из букв русского алфавита '
    'и может содержать дефисы.'
)


def validate_non_empty(value: str, allow_none: bool = False):
    if value is None:
        if allow_none:
            return
        return ValueError(NON_EMPTY)
    if not value.strip():
        raise ValueError(NON_EMPTY)
    return value

def validate_english_word(value: str, allow_none: bool = False):
    if value is None:
        if allow_none:
            return
        return ValueError(NON_EMPTY)
    if not match(ENGLISH_WORD_PATTERN, value.strip().lower()):
        raise ValueError(ENGLISH_WORD_ERROR)
    return value

def validate_russian_word(value: str, allow_none: bool = False):
    if value is None:
        if allow_none:
            return
        return ValueError(NON_EMPTY)
    if not match(RUSSIAN_WORD_PATTERN, value.strip().lower()):
        raise ValueError(RUSSIAN_WORD_ERROR)
    return value
