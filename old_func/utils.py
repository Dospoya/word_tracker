import json
import os
import random
from typing import List, Union

from .word import Word

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WORDS_PATH = os.path.join(BASE_DIR, "words.json")


# Функционал для сохранения и загрузки слов из БД в файл
def load_json(
) -> List[Word]:
    with open(WORDS_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(data: List[Word]) -> None:
    with open(WORDS_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# Функционал для повторения слов
def get_random_word() -> Union[str, Word]:
    not_done_words = [
        word for word in load_json() if not word.get('done', False)
    ]
    if not not_done_words:
        return 'Все слова выучены'
    return random.choice(not_done_words)

def note_as_done(target_word: str) -> None:
    data = load_json()
    for word in data:
        if word['word'] == target_word:
            word['done'] = True
            break
    save_json(data)

# Функционал для отслежования прогресса
def get_progress() -> str:
    data = load_json()
    progress_count = 0
    for word in data:
        if word['done'] == True:
            progress_count += 1
    return f'Ты выучил {progress_count} слов из {len(data)}'
