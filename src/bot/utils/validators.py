import re

NAME_REGEX = re.compile(r'^[А-ЯЁ][а-яё]+(-[А-ЯЁ][а-яё]+)?$')


def is_valid_russian_name(name: str) -> bool:
    name = name.strip().capitalize()
    return (
        2 <= len(name) <= 30
        and ' ' not in name
        and bool(NAME_REGEX.fullmatch(name))
    )
