from artofmemory import convert_word_to_major

import unittest

class TestArtOfMemory(unittest.TestCase):
    '''
    Here is my adapted major system

    Digit   Letter
    0   s, z
    1   t, d
    2   n
    3   m
    4   r
    5   l
    6   j, g
    7   c, k, q, 
    8   v, f
    9   p, b

    e.g. satellite => 0151

    '''
    def test_ts(self):
        ret = convert_word_to_major('test')
        self.assertEqual(ret, '101')

    def test_word_with_ph(self):
        ret = convert_word_to_major('phone')
        self.assertEqual(ret, '92')
       
    def test_word_with_ch(self):
        ret = convert_word_to_major('chad')
        self.assertEqual(ret, '71')

    def test_word_with_ck(self):
        ret = convert_word_to_major('jack')
        self.assertEqual(ret, '677')

    def test_word_with_sh(self):
        ret = convert_word_to_major('shut')
        self.assertEqual(ret, '01')

    def test_word_with_th(self):
        ret = convert_word_to_major('the')
        self.assertEqual(ret, '1')

    def test_word_with_double_letter(self):
        ret = convert_word_to_major('basketball')
        self.assertEqual(ret, '9071955')

if __name__ == '__main__':
    unittest.main()
