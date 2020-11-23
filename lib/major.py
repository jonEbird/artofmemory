import itertools
import random
import re

from .words import COMMON_WORDS_EN


class NaiveMajorSystem(object):
    """A naive implementation of the major system.

    Does not consider differences between soft and hard sounding consonants.
    """

    MAPPING = {
        0: ["s", "z"],
        1: ["t", "d"],
        2: ["n"],
        3: ["m"],
        4: ["r"],
        5: ["l"],
        6: ["j", "g"],
        7: ["c", "k", "q"],
        8: ["v", "f"],
        9: ["p", "b"],
    }

    def __init__(self):
        self.major_letters = list(itertools.chain(*self.MAPPING.values()))

    def _regex_from_letter_mapping(self):
        """
        Given a dictionary of number to character mappings, return a regular
        expression that can be used to break it up
        """

        all_letters = itertools.chain(*self.MAPPING.values())

        sorted_letters = sorted(all_letters, key=lambda x: len(x), reverse=True)

        # This will looks like '(th|ch|sh|k|....)
        regex = "({})".format("|".join(sorted_letters))

        return regex

    def word_to_major(self, word: str) -> str:
        """Given a word, convert it to the major system.

        e.g. satellite => 0151

        @param  word        Word to convert
        @returns    int     Integer value of given word
        """
        regex = self._regex_from_letter_mapping()

        value = ""
        for piece in re.findall(regex, word):
            for i, letters in self.MAPPING.items():
                if piece.lower() in letters:
                    value += str(i)
        return value


def basic_quiz(use_letters: bool = True):
    """Quiz converting words to major numeric equivalent"""
    game = "letters" if use_letters else "words"

    naive_system = NaiveMajorSystem()

    words = COMMON_WORDS_EN
    correct = 0
    total = 0
    while True:
        try:
            if game == "words":
                word = random.choice(words)
            elif game == "letters":
                word = random.choice(list(NaiveMajorSystem.MAPPING.keys()))
            major_value = naive_system.word_to_major(word)

            guess = input("{} => ".format(word))
            if not guess:
                continue
            if guess == str(major_value):
                print("Correct!")
                correct += 1
            else:
                print("Nope, it is {}".format(major_value))
            total += 1

        except KeyboardInterrupt:
            if total:
                print("\n{:>2}% Correct".format(correct / float(total) * 100))
            break
