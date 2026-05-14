from typing import TypedDict


class MeaningsTD(TypedDict):
    pos: str
    examples: list[str]
    synonyms: list[str]
    definition: str


class Entry(TypedDict):
    id: int
    word: str
    meanings: list[MeaningsTD]
    antonyms: list[str]
    synonyms: list[str]
    count: int


def _clip(text: str, limit: int) -> str:
    text = text.strip()
    if len(text) < limit:
        return text
    return text[: limit - 1] + "..."


def format_entry(entry: Entry | None, short_definition: bool = False) -> str | None:
    if entry is None:
        return None
    lines: list[str] = []
    word: str = entry.get("word", "")
    lines.append(f"📘 Word: {word}")
    meanings: list[MeaningsTD] = entry.get("meanings") or []
    general_antonyms: list[str] = entry.get("antonyms") or []
    general_synonyms: list[str] = entry.get("synonyms") or []
    if not meanings:
        lines.append("📖 Definition: значений слова не найдено")
        if general_antonyms:
            lines.append(f"Antonyms: {', '.join(general_antonyms)}")
        if general_synonyms:
            lines.append(f"Synonyms: {', '.join(general_synonyms)}")
        return "\n".join(lines)
    if short_definition:
        meaning: MeaningsTD = meanings[0]
        pos: str = meaning.get("pos", "")
        if pos:
            lines.append(f"💡 Part of Speech: {pos}")
        definition: str = _clip(meaning.get("definition", ""), 100)
        if definition:
            lines.append(f"📖 Definition: {definition}")
        examples_text = ",\n".join(meaning.get("examples", []))
        if examples_text:
            lines.append(f"💡 Examples: {examples_text}")
        synonyms = ", ".join(meaning.get("synonyms", []))
        if synonyms:
            lines.append(f"Synonyms: {synonyms}")
        return "\n".join(lines)

    for index, meaning in enumerate(meanings[:3], start=1):
        pos = meaning.get("pos", "")
        definition = _clip(meaning.get("definition", ""), 180)
        title = f"{index}. {pos}" if pos else f"{index}."
        lines.append(title)
        if definition:
            lines.append(f"   {definition}")
        examples = meaning.get("examples", [])
        if examples:
            lines.append(f"   Example: {_clip(examples[0], 140)}")
        local_synonyms = meaning.get("synonyms", [])
        if local_synonyms:
            lines.append(f"   Synonyms: {', '.join(local_synonyms[:5])}")

    if general_synonyms:
        lines.append(f"Common synonyms: {', '.join(general_synonyms[:8])}")
    if general_antonyms:
        lines.append(f"Antonyms: {', '.join(general_antonyms[:8])}")
    return "\n".join(lines)
