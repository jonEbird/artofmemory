import itertools
import random
import re
from typing import List, Tuple

import pronouncing
from nltk.corpus import wordnet as wn

from .data.words import COMMON_WORDS_EN


class MajorSystem(object):
    """The Major system is a peg system for numbers <--> words.

    It is a system where each digit has one or more consonants that can represent it. You
    can then substitute digits in a number for letters and fill in whichever vowels you'd
    like to form words. When a consonant is not included in the system, it also can be
    used as filler letters such as 'w' or 'h'.

    When there are multiple constants for a digit, it is because they both roughly make
    the same sound when pronounced. Lets take the digit 1 for which we can substitute
    either 'd' or 't'. When you make the sound of either letter, your mouth and tongue are
    positioned the same and hence are considered equivalent in this system.

    Here is the mapping:

    0 -> s, z, soft 'c'
    1 -> d, t
    2 -> n
    3 -> m
    4 -> r
    5 -> l
    6 -> j, ch, sh, soft 'g'
    7 -> hard 'c', k, hard 'g'
    8 -> f, v
    9 -> b, p

    Examples:

    letter => 514
    You do not repeat the 1 even though there are two 't's because the sound you make is
    just a single 't' sound.

    circle => 0475
    The first 'c' is soft, so you use a 0 which sounds like 's' and the second 'c' is
    hard.
    """

    def word_to_major(self, word: str) -> str:
        raise NotImplementedError

    def number_to_words(self, number: str) -> List[str]:
        raise NotImplementedError


class PhonemesMajorSystem(MajorSystem):
    """An implementation of the major system that uses phonemes.

    Breaks up words based on their actual phonetic sounds (phonemes).
    """

    MAPPING = {
        0: ["S", "Z"],
        1: ["T", "D"],
        2: ["N", "NG"],  # Including "NG" as in "finger"
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

        # FIXME: This whole implementation is basically a special form of
        #        pronouncing.search() and hence needs to call .init_cmu(). Ideally this
        #        detail is not needed.
        pronouncing.init_cmu()

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


class NaiveMajorSystem(MajorSystem):
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


def basic_quiz(use_letters: bool = False):
    """Quiz converting words to major numeric equivalent"""
    game = "letters" if use_letters else "words"

    major_system = PhonemesMajorSystem()

    words = COMMON_WORDS_EN
    correct = 0
    total = 0
    while True:
        if game == "words":
            word = random.choice(words)
        elif game == "letters":
            word = str(random.choice(list(NaiveMajorSystem.MAPPING.keys())))
        major_value = major_system.word_to_major(word)

        try:
            guess = input("{} => ".format(word))
        except (EOFError, KeyboardInterrupt):
            break

        if guess == str(major_value):
            print("Correct!")
            correct += 1
        else:
            print("Nope, it is {}".format(major_value))
        total += 1

    if total:
        print("\n{:>2}% Correct".format(correct / float(total) * 100))


def explain() -> str:
    """Provide an explanation summary of the system"""
    return "\n".join(map(lambda l: l.lstrip(), str(MajorSystem.__doc__).split("\n")))


def print_number_words(numbers: Tuple[str], nouns_only: bool = False) -> None:
    """Print out a series of possible words that can match the given numbers."""
    major = PhonemesMajorSystem()

    if nouns_only:
        nouns = {x.name().split(".", 1)[0] for x in wn.all_synsets("n")}

    for number in numbers:
        if number.isdigit():
            words = major.number_to_words(number)
            if nouns_only:
                words = list(filter(lambda word: word in nouns, words))
            print(f"{number}: {', '.join(words)}\n")
        else:
            # looking to translate the word
            word = number
            print(f"{word}: {major.word_to_major(word)}\n")
