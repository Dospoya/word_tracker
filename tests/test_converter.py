import unittest

from bot.services.converter import format_entry

ENTRY = {
    "id": 1,
    "word": "abandon",
    "meanings": [
        {
            "pos": "Verb",
            "definition": "to leave someone or something completely",
            "examples": ["They had to abandon the car in the snow."],
            "synonyms": ["leave", "desert"],
        },
        {
            "pos": "Noun",
            "definition": "freedom from inhibition or restraint",
            "examples": ["She sang with joyful abandon."],
            "synonyms": ["freedom"],
        },
    ],
    "antonyms": ["keep"],
    "synonyms": ["leave", "desert", "forsake"],
    "count": 3,
}


class FormatEntryTests(unittest.TestCase):
    def test_short_definition_uses_meaning_level_examples_and_synonyms(self):
        rendered = format_entry(ENTRY, short_definition=True)

        self.assertIsNotNone(rendered)
        self.assertIn("📘 Word: abandon", rendered)
        self.assertIn("💡 Part of Speech: Verb", rendered)
        self.assertIn("💡 Examples: They had to abandon the car in the snow.", rendered)
        self.assertIn("Synonyms: leave, desert", rendered)
        self.assertNotIn("forsake", rendered)

    def test_full_definition_renders_multiple_meanings(self):
        rendered = format_entry(ENTRY)

        self.assertIsNotNone(rendered)
        self.assertIn("1. Verb", rendered)
        self.assertIn("2. Noun", rendered)
        self.assertIn("Example: They had to abandon the car in the snow.", rendered)
        self.assertIn("Common synonyms: leave, desert, forsake", rendered)
        self.assertIn("Antonyms: keep", rendered)

    def test_none_entry_returns_none(self):
        self.assertIsNone(format_entry(None))


if __name__ == "__main__":
    unittest.main()
