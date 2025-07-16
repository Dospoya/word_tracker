import json
import openai

from .wictionary import WiktionaryEntry
from .templates import render_template
from src.app.core.config import settings

CONVERTER_SYSTEM_PROMPT = render_template("instruction.md.jinja2")


def converter(obj_in: dict) -> WiktionaryEntry | None:
    client = openai.OpenAI(api_key=settings.openai_api_key)
    response = client.responses.parse(
        model='gpt-4o-mini',
        input=[
            {
                'role': 'system',
                'content': CONVERTER_SYSTEM_PROMPT,
            },
            {
                'role': 'user',
                'content': json.dumps(obj_in)
            }
        ],
        text_format=WiktionaryEntry
    )
    return response.output_parsed
