import unittest

from lib.major import NaiveMajorSystem


class TestArtOfMemory(unittest.TestCase):
    """
    Test all the things in artofmemory.py
    """

    def test_ts(self):
        ret = NaiveMajorSystem().word_to_major("test")
        self.assertEqual(ret, "101")

    def test_word_with_ph(self):
        ret = NaiveMajorSystem().word_to_major("phone")
        self.assertEqual(ret, "92")

    def test_word_with_ch(self):
        ret = NaiveMajorSystem().word_to_major("chad")
        self.assertEqual(ret, "71")

    def test_word_with_ck(self):
        ret = NaiveMajorSystem().word_to_major("jack")
        self.assertEqual(ret, "677")

    def test_word_with_sh(self):
        ret = NaiveMajorSystem().word_to_major("shut")
        self.assertEqual(ret, "01")

    def test_word_with_th(self):
        ret = NaiveMajorSystem().word_to_major("the")
        self.assertEqual(ret, "1")

    def test_word_with_double_letter(self):
        ret = NaiveMajorSystem().word_to_major("basketball")
        self.assertEqual(ret, "9071955")

    def test_regex_builder_empty(self):
        ms = NaiveMajorSystem()
        ms.MAPPING = {}
        ret = ms._regex_from_letter_mapping()
        self.assertEqual(ret, "()")

    def test_regex_builder_full(self):
        ret = NaiveMajorSystem()._regex_from_letter_mapping()
        self.assertEqual(ret, "(s|z|t|d|n|m|r|l|j|g|c|k|q|v|f|p|b)")
