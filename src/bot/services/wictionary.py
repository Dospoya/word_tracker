# from pydantic import BaseModel

# from bot.services.apiclient import APIClient

# WICTONARY_BASE_URL = "https://en.wiktionary.org"
# WIKTIONARY_API_URL = (
#     "/w/api.php?action=query&format=json&prop=extracts&titles={word}&redirects=1"
# )


# class DefinitionMixin(BaseModel):
#     definition: list[str] | None = None


# class PronunciationModel(BaseModel):
#     enPR: str
#     IPA: str
#     rhymes: str


# class TranslationModel(BaseModel):
#     russian: str


# class NounFormsModel(BaseModel):
#     countability: str | None = None
#     plural: str | None = None


# class NounDefinitionModel(DefinitionMixin):
#     pass


# class NounModel(BaseModel):
#     forms: NounFormsModel | None = None
#     definitions: NounDefinitionModel | None
#     translations: TranslationModel


# class VerbFormsModel(BaseModel):
#     third_person_singular: str | None = None
#     present_participle: str | None = None
#     simple_past_past_participle: str | None = None


# class VerbDefinitionModel(DefinitionMixin):
#     pass


# class VerbModel(BaseModel):
#     forms: VerbFormsModel | None = None
#     definitions: list[VerbDefinitionModel]
#     translations: TranslationModel


# class ContentModel(BaseModel):
#     language: str
#     alternative_forms: list[str] | None = None
#     etymology: str | None = None
#     pronunciation: PronunciationModel | None = None
#     noun: NounModel | None = None
#     verb: VerbModel | None = None


# class WiktionaryEntry(BaseModel):
#     pageid: int
#     ns: int
#     title: str
#     content: ContentModel


# async def get_wictionary_word(word: str) -> dict | None:
#     async with APIClient(base_url=WICTONARY_BASE_URL) as client:
#         response = await client.get(
#             path=WIKTIONARY_API_URL.format(word=word),
#             include_auth_headers=False,
#         )
#         return response

# import json

# import openai

# from app.core.config import settings

# from .templates import render_template
# from .wictionary import WiktionaryEntry

# CONVERTER_SYSTEM_PROMPT = render_template("instruction.md.jinja2")


# def converter(obj_in: dict) -> WiktionaryEntry | None:
#     client = openai.OpenAI(api_key=settings.openai_api_key)
#     response = client.responses.parse(
#         model="gpt-4o-mini",
#         input=[
#             {
#                 "role": "system",
#                 "content": CONVERTER_SYSTEM_PROMPT,
#             },
#             {"role": "user", "content": json.dumps(obj_in)},
#         ],
#         text_format=WiktionaryEntry,
#     )
#     return response.output_parsed
