from artofmemory import convert_word_to_major

import unittest

class TestArtOfMemory(unittest.TestCase):
    '''
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

    '''
    def test_simple(self):
        ret = convert_word_to_major('test')
        self.assertEqual(ret, 101)

    def test_word_with_ph(self):
        ret = convert_word_to_major('phone')
        self.assertEqual(ret, 82)
       
    def test_word_with_ch(self):
        ret = convert_word_to_major('chad')
        self.assertEqual(ret, 61)

    def test_word_with_ck(self):
        ret = convert_word_to_major('jack')
        self.assertEqual(ret, 67)

    def test_word_with_sh(self):
        ret = convert_word_to_major('shut')
        self.assertEqual(ret, 61)

    def test_word_with_th(self):
        ret = convert_word_to_major('the')
        self.assertEqual(ret, 1)

    def test_word_with_double_letter(self):
        ret = convert_word_to_major('basketball')
        self.assertEqual(ret, 907195)

if __name__ == '__main__':
    unittest.main()
