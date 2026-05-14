import importlib
import unittest


class ImportSmokeTests(unittest.TestCase):
    def test_vocabulary_router_imports(self):
        module = importlib.import_module("bot.handlers.user.vocab")
        self.assertTrue(hasattr(module, "vocabulary_router"))


if __name__ == "__main__":
    unittest.main()
