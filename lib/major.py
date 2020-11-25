import itertools
import random
import re
from typing import List

import pronouncing

from .words import COMMON_WORDS_EN


class PhonemesMajorSystem(object):
    """An implementation of the major system that uses phonemes.

    Breaks up words based on their actual phonetic sounds (phonemes).
    """

    MAPPING = {
        0: ["S", "Z"],
        1: ["T", "D"],
        2: ["N"],  # "NG" as in "finger"?
        3: ["M"],
        4: ["R", "ER0", "ER1"],
        5: ["L"],
        6: ["JH", "CH", "SH"],
        7: ["K", "G"],
        8: ["F", "V"],
        9: ["B", "P"],
    }

    def __init__(self):
        # Create a reverse map for quick lookup
        self.phonemes2num = {}
        for num, phonemes in self.MAPPING.items():
            for phoneme in phonemes:
                self.phonemes2num[phoneme] = num

    def word_to_major(self, word: str) -> str:
        """Convert word to phonetic major-system value."""
        phonemes = pronouncing.phones_for_word(word)
        if not phonemes:
            return ""

        return "".join(
            [
                str(self.phonemes2num[p])
                for p in phonemes[0].split()
                if p in self.phonemes2num
            ]
        )

    def number_to_words(self, number: str) -> List[str]:
        """Return a list of possible word matches for the given number."""
        # pronouncing.pronunciations is a list
        # pronouncing.lookup is a dict mapping of the word to the phonemes

        # 83 should match "FM" and "VM"

        pattern = "^"
        for n in map(int, re.findall(r"\d", number)):
            pattern += f"({'|'.join(self.MAPPING[n])})"
        pattern += "$"

        matcher = re.compile(pattern)

        matches = []
        for word, phonemes in pronouncing.pronunciations:
            consts = "".join(
                filter(lambda p: p in self.phonemes2num.keys(), phonemes.split())
            )
            if matcher.match(consts):
                matches.append(word)

        return matches


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


def basic_quiz(use_letters: bool = True, use_naive: bool = False):
    """Quiz converting words to major numeric equivalent"""
    game = "letters" if use_letters else "words"

    if use_naive:
        major_system = NaiveMajorSystem()
    else:
        major_system = PhonemesMajorSystem()

    words = COMMON_WORDS_EN
    correct = 0
    total = 0
    while True:
        try:
            if game == "words":
                word = random.choice(words)
            elif game == "letters":
                word = str(random.choice(list(NaiveMajorSystem.MAPPING.keys())))
            major_value = major_system.word_to_major(word)

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
