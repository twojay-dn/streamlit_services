from srcs.utils import load_words
import random

class WordsPool:
    @classmethod
    def init(cls):
        cls.words = load_words()

    @classmethod
    def get_random_word(cls):
        return random.choice(cls.words)