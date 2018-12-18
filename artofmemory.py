#!/bin/env python3

import configparser
import itertools
import os
import random
import re

import click

from lib.common import MOST_COMMON_WORDS

default_major_map = {0: ['s', 'z'],
                     1: ['t', 'd'],
                     2: ['n'],
                     3: ['m'],
                     4: ['r'],
                     5: ['l'],
                     6: ['j', 'g'],
                     7: ['c', 'k', 'q'],
                     8: ['v', 'f'],
                     9: ['p', 'b']}

major_letters = list(itertools.chain(*default_major_map.values()))


class Person(object):
    pass


class Action(object):
    pass


class Object(object):
    pass


def get_artofmemory_config(filename):
    '''
    Given a filename, return a configparser object with the config contents

    @param  str     filename        Where is the config located
    @return ConfigParser            ConfigParser object
    '''
    config = configparser.ConfigParser()
    fname = os.path.expanduser(filename)
    try:
        config.readfp(open(fname))
    except IOError:
        print('Unable to read config file: {}'.format(fname))
    return config


def build_regex_from_letter_mapping(major_map):
    '''
    Given a dictionary of number to character mappings, return a regular
    expression that can be used to break it up
    '''

    all_letters = itertools.chain(*major_map.values())

    sorted_letters = sorted(all_letters, key=lambda x: len(x), reverse=True)

    # This will looks like '(th|ch|sh|k|....)
    regex = '({})'.format('|'.join(sorted_letters))

    return regex


def convert_word_to_major(word, major_map=default_major_map):
    '''
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
    '''
    regex = build_regex_from_letter_mapping(major_map)

    value = ''
    for piece in re.findall(regex, word):
        for i, letters in major_map.items():
            if piece.lower() in letters:
                value += str(i)
    return value


class Card(object):
    suits = {'club': '\u2663',
             'spade': '\u2660',
             'heart': '\u2764',
             'diamond': '\u2666',
             }

    values = {1: 'A',
              2: '2',
              3: '3',
              4: '4',
              5: '5',
              6: '6',
              7: '7',
              8: '8',
              9: '9',
              10: '10',
              11: 'J',
              12: 'Q',
              13: 'K',
              }

    def __init__(self, value, suit):
        self.value = value
        self.suit = self.suits[suit]

    def __repr__(self):
        # TODO(shuff): Add proper colors
        return "{0}{1.suit}".format(self.values[self.value], self)


def play_major_system(game='words', letter_mapping=default_major_map):
    '''
    Play a simple game using the major system to convert words to their
    major numeric equivalent
    '''
    words = MOST_COMMON_WORDS
    correct = 0
    total = 0
    while True:
        if game == 'words':
            word = list(words)[random.randint(0, len(words) - 1)]
        elif game == 'letters':
            word = major_letters[random.randint(0, len(major_letters) - 1)]

        try:
            guess = input('{} => '.format(word, end=''))
        except KeyboardInterrupt:
            print('\n{:>2}% Correct'.format(correct / float(total) * 100))
            break

        major_value = convert_word_to_major(word)
        if not guess:
            continue
        if guess == str(major_value):
            print('CORRECT!')
            correct += 1
        else:
            print('INCORRECT: {}'.format(major_value))
        total += 1


def play_poa(config, shuffle=False):
    '''
    Test out your POA skills.  It supports just testing your POA + shuffling
    them up to test combos
    '''
    # TODO -- add an option to limit the values to test
    # e.g. if I only want to test POA for 1 through 4

    # TODO add support for properly mixing up the POA and testing
    if 'poa' not in config.sections():
        print('No POA Config setup.  See README')

    poa_section = config['poa']

    poa_mapping = list(poa_section.items())

    correct = 0
    total = 0
    while True:
        # Grab a random section
        number, poa = poa_mapping[random.randint(0, len(poa_mapping) - 1)]
        poa = ' '.join(poa.split(','))
        try:
            guess = input('{}\n=> '.format(poa))
        except KeyboardInterrupt:
            print('\n{:>2}% Correct'.format(correct / float(total) * 100))
            break
        if not guess:
            continue
        if guess == number:
            print('CORRECT!')
            correct += 1
        else:
            print('INCORRECT: {}'.format(number))
        total += 1


def _do_main(major_system,
             letters,
             cards,
             poa,
             print_conf,
             filename):

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
            print('Failed to read config')

    elif major_system:
        game = 'letters' if letters else 'words'
        play_major_system(game)
    elif poa:
        play_poa(config)
    else:
        # TODO -- Print out proper click help test
        print('click HELP')


@click.command()
@click.option('--major-system', is_flag=True)
@click.option('--letters', is_flag=True)
@click.option('--cards', is_flag=True)
@click.option('--poa', is_flag=True)
@click.option('--print-conf', is_flag=True)
@click.option('--filename', type=str, default='~/.artofmemory.conf')
def main(major_system, letters, cards, poa, print_conf, filename):
    _do_main(major_system, letters, cards, poa, print_conf, filename)


if __name__ == '__main__':
    main()
