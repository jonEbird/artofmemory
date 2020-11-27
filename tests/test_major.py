"""Ensure testing of the Major System does what we expect"""

from artofmemory.major import NaiveMajorSystem, PhonemesMajorSystem


def test_office():
    # office shouldn't be "887" but rather actually "80"!
    naive_value = "887"
    correct_value = "80"

    assert NaiveMajorSystem().word_to_major("office") == naive_value
    assert PhonemesMajorSystem().word_to_major("office") == correct_value

    # Other tricky words:
    # passage, Alexander

    # burn => 942, Nope, it is 92
