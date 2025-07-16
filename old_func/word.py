from typing import List, TypedDict

class Word(TypedDict):
    id: int
    word: str
    synonyms: List[str]
    example: str
    done: bool
