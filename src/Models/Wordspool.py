from src.utils import load_words
import random

class WordsPool:
    @classmethod
    def init(cls):
        cls.words = load_words()

    @classmethod
    def get_random_word(cls):
        if not hasattr(cls, "words"):
            cls.init()
        return random.choice(cls.words)