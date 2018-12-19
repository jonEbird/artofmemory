# -*- coding: utf-8 -*-


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
