#!/usr/bin/env python3

import configparser
import itertools
import os
import random
import re

import click

from lib.common import MOST_COMMON_WORDS
from lib.cards import Card

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


def get_artofmemory_config(filename):
    """
    Given a filename, return a configparser object with the config contents

    @param  str     filename        Where is the config located
    @return ConfigParser            ConfigParser object
    """
    config = configparser.ConfigParser()
    fname = os.path.expanduser(filename)
    try:
        config.read_file(open(fname))
    except IOError:
        print("Unable to read config file: {}".format(fname))
    return config


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


def play_major_system(game="words", letter_mapping=default_major_map):
    """
    Play a simple game using the major system to convert words to their
    major numeric equivalent
    """
    words = MOST_COMMON_WORDS
    correct = 0
    total = 0
    while True:
        if game == "words":
            word = list(words)[random.randint(0, len(words) - 1)]
        elif game == "letters":
            word = major_letters[random.randint(0, len(major_letters) - 1)]

        try:
            guess = input("{} => ".format(word), end="")
        except KeyboardInterrupt:
            print("\n{:>2}% Correct".format(correct / float(total) * 100))
            break

        major_value = convert_word_to_major(word)
        if not guess:
            continue
        if guess == str(major_value):
            print("CORRECT!")
            correct += 1
        else:
            print("INCORRECT: {}".format(major_value))
        total += 1


def flatten_pao(d):
    """Yield back (num, item) tuples for each PAO broken into items.

    The PAO item will be prefixed with either 'p:', 'a:', 'o:' to help denote its part of
    the overall PAO.

    Args:
        d (dict): dictionary-like object that supports .items()
    Yields:
        (str, str)
    """
    for num, pao in d.items():
        person, action, obj = pao.split(",")
        yield (num, "p:" + person.strip())
        yield (num, "a:" + action.strip())
        yield (num, "o:" + obj.strip())


def play_pao(config, shuffle=False):
    """Test out your Person Action Object (PAO) skills.

    It supports just testing your PAO + shuffling them up to test combos
    """
    # TODO -- add an option to limit the values to test
    # e.g. if I only want to test PAO for 1 through 4

    # TODO add support for properly mixing up the PAO and testing
    if "pao" not in config.sections():
        print("No PAO Config setup.  See README")
        return

    pao_pairs = list(flatten_pao(config["pao"]))

    correct = 0
    total = 0
    try:
        while True:
            # Randomize the PAO items
            random.shuffle(pao_pairs)

            for number, item in pao_pairs:
                guess = input("{}\n=> ".format(item))
                if not guess:
                    continue
                if guess == number:
                    print("CORRECT!")
                    correct += 1
                else:
                    print("INCORRECT: {}".format(number))
                total += 1
    except KeyboardInterrupt:
        if total:
            print("\n{:>2}% Correct".format(correct / float(total) * 100))


def _do_main(major_system, letters, cards, pao, print_conf, filename):

    config = get_artofmemory_config(filename)
    if cards:
        value = random.randint(1, 13)
        suit = list(Card.suits.keys())[random.randint(0, 3)]
        print(Card(value, suit))
    elif print_conf:
        try:
            with open(os.path.expanduser(filename)) as of:
                print(of.read())
        except IOError:
            print("Failed to read config")

    elif major_system:
        game = "letters" if letters else "words"
        play_major_system(game)
    elif pao:
        play_pao(config)
    else:
        # TODO -- Print out proper click help test
        print("click HELP")


@click.command()
@click.option("--major-system", is_flag=True)
@click.option("--letters", is_flag=True)
@click.option("--cards", is_flag=True)
@click.option("--pao", is_flag=True)
@click.option("--print-conf", is_flag=True)
@click.option("--filename", type=str, default="~/.artofmemory.conf")
def main(major_system, letters, cards, pao, print_conf, filename):
    _do_main(major_system, letters, cards, pao, print_conf, filename)


if __name__ == "__main__":
    main()
