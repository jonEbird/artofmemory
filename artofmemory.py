#!/bin/env python3

import click
import itertools
import random

#  Numeral Associated Consonants   Mnemonic
#  0   s, z, soft c    z is the first letter of zero. The other letters have a similar sound.
#  1   t, d    d & t have one downstroke and sound similar (some variant systems include "th")
#  2   n   n has two downstrokes and looks something like "2" on its side
#  3   m   M has three downstrokes and looks like a 3 on its side
#  4   r   last letter of four, also 4 and R are almost mirror images of each other
#  5   l   L is the Roman Numeral for 50
#  6   sh, soft ch, j, soft g, zh  a script j has a lower loop / g is almost a 6 flipped over
#  7   k, hard c, hard g, hard ch, q, qu   capital K "contains" two sevens
#  8   f, v    script f resembles a figure-8. V sounds similar. (some variant systems include th)
#  9   p, b    p is a mirror-image 9. b sounds similar and resembles a 9 rolled around
#  Unassigned  Vowel sounds, w,h,y These can be used anywhere without changing a word's number value

class Person(object):
    pass


class Action(object):
    pass


class Object(object):
    pass

def convert_word_to_major(word):
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
    letter_to_integer = {0: ['s', 'z'],
                            1: ['t', 'd', 'th'],
                            2: ['n'],
                            3: ['m'],
                            4: ['r'],
                            5: ['l'],
                            6: ['j', 'ch', 'sh'],
                            7: ['c', 'k', 'g', 'q', 'ck'],
                            8: ['v', 'f', 'ph'],
                            9: ['p', 'b']}
    value = ''
    for c in word:
        for i,letters in letter_to_integer.items():
            if c in letters:
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

@click.command()
@click.option('--major-system', is_flag=True)
@click.option('--cards', is_flag=True)
def main(major_system, cards):
    if cards:
        value = random.randint(1,13)
        suit = list(Card.suits.keys())[random.randint(0, 3)]
        print(Card(value, suit))
    if major_system:
       words = open('/usr/share/dict/words').read().split()
       word = list(words)[random.randint(0, len(words) - 1)]
       print('{0} => {1}'.format(word, convert_word_to_major(word)) )

if __name__ == '__main__':
    main()

