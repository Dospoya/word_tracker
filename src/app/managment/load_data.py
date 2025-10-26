import asyncio
import json
import logging
from pathlib import Path
from typing import Any

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio.session import AsyncSession

from app.core.db import AsyncSessionLocal
from app.models.global_word import GlobalWord

logging.basicConfig(
    level=logging.INFO, format="%(levelname)s - %(asctime)s - %(message)s"
)

FILE_DIR = "data"
FILE_NAME = "filtered.json"

BASE_DIR = Path(__file__).resolve().parent.parent.parent
FILE_PATH = BASE_DIR / FILE_DIR / FILE_NAME


def _map_meanings(item: list[Any]) -> dict[str, str | list[str]]:
    if len(item) < 2:
        return {"pos": "", "definition": "", "synonyms": [], "examples": []}
    pos = item[0] if isinstance(item[0], str) else ""
    definition = item[1] if isinstance(item[1], str) else ""
    synonyms: list[str] = item[2] if len(item) > 2 and isinstance(item[2], list) else []
    examples: list[str] = item[3] if len(item) > 3 and isinstance(item[3], list) else []
    if not pos or not definition:
        return {}
    return {
        "pos": pos,
        "definition": definition,
        "synonyms": [s for s in synonyms],
        "examples": [ex for ex in examples],
    }


async def load_data_from_json(session: AsyncSession) -> dict[str, int]:
    total = inserted = skipped = 0
    try:
        with open(FILE_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        batch = 0
        for word, payload in data.items():
            total += 1
            w = (word or "").strip().lower()
            if not isinstance(payload, dict) or not w:
                skipped += 1
                continue
            raw_meanings = payload.get("MEANINGS", [])
            meanings: list[dict] = []
            for m in raw_meanings:
                mapped = _map_meanings(m)
                if mapped:
                    meanings.append(mapped)
            antonyms = payload.get("ANTONYMS", [])
            synonyms = payload.get("SYNONYMS", [])
            if not meanings and not antonyms and not synonyms:
                skipped += 1
                continue
            session.add(
                GlobalWord(
                    word=w,
                    meanings=meanings,
                    antonyms=[a for a in antonyms if isinstance(a, str)],
                    synonyms=[s for s in synonyms if isinstance(s, str)],
                )
            )
            batch += 1
            if batch % 1000 == 0:
                try:
                    await session.flush()
                    await session.commit()
                    inserted += batch
                    batch = 0
                except IntegrityError:
                    await session.rollback()
                    skipped += 1
                    batch = 0
        if batch:
            try:
                await session.flush()
                await session.commit()
                inserted += batch
            except IntegrityError:
                await session.rollback()
                skipped += 1
        logging.info(
            f"Пропущено {skipped} слов. Добавлено {inserted} слов. Всего {total}"
        )
        return {"total": total, "inserted": inserted, "skipped": skipped}
    except Exception as e:
        logging.exception(f"Не удалось открыть файл {FILE_PATH} ошибка {e}")
        return {"total": total, "inserted": inserted, "skipped": skipped}


if __name__ == "__main__":

    async def main():
        async with AsyncSessionLocal() as session:
            await load_data_from_json(session)

    asyncio.run(main())
