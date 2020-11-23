import itertools
import random
import re

from .words import COMMON_WORDS_EN

default_major_map = {
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

major_letters = list(itertools.chain(*default_major_map.values()))


def build_regex_from_letter_mapping(major_map):
    """
    Given a dictionary of number to character mappings, return a regular
    expression that can be used to break it up
    """

    all_letters = itertools.chain(*major_map.values())

    sorted_letters = sorted(all_letters, key=lambda x: len(x), reverse=True)

    # This will looks like '(th|ch|sh|k|....)
    regex = "({})".format("|".join(sorted_letters))

    return regex


def convert_word_to_major(word, major_map=default_major_map):
    """
    Given a word, convert it to the major system.

    Here is the approximte major system

    Digit   Letter
    0   s, z
    1   t, d, th
    2   n
    3   m
    4   r
    5   l
    6   j, ch, sh
    7   c, k, g, q, ck
    8   v, f, ph
    9   p, b

    e.g. satellite => 0151

    @param  word        Word to convert
    @returns    int     Integer value of given word
    """
    regex = build_regex_from_letter_mapping(major_map)

    value = ""
    for piece in re.findall(regex, word):
        for i, letters in major_map.items():
            if piece.lower() in letters:
                value += str(i)
    return value


def basic_quiz(use_letters: bool = True, letter_mapping=default_major_map):
    """Quiz converting words to major numeric equivalent"""
    game = "letters" if use_letters else "words"

    words = COMMON_WORDS_EN
    correct = 0
    total = 0
    while True:
        if game == "words":
            word = list(words)[random.randint(0, len(words) - 1)]
        elif game == "letters":
            word = major_letters[random.randint(0, len(major_letters) - 1)]

        try:
            guess = input("{} => ".format(word))
        except KeyboardInterrupt:
            if total:
                print("\n{:>2}% Correct".format(correct / float(total) * 100))
            break

        major_value = convert_word_to_major(word)
        if not guess:
            continue
        if guess == str(major_value):
            print("Correct!")
            correct += 1
        else:
            print("Nope, it is {}".format(major_value))
        total += 1
