#!/usr/bin/env python3

import os

import click

from artofmemory.cards import random_card
from artofmemory.data import bible
from artofmemory.major import basic_quiz, print_number_words
from artofmemory.pao import pao_quiz
from artofmemory.missing import quiz_missing


@click.group()
def quiz():
    pass


@quiz.command("bible")
@click.option("--say/--no-say", default=False)
def books_of_bible(say: bool):
    """Guess which book is missing from Bible"""
    quiz_missing(bible.old_testament + bible.new_testament, talk=say)


@quiz.command()
@click.option("--naive/--no-naive", default=False)
@click.option("--letters/--no-letters", default=False)
def major_system(letters: bool, naive: bool):
    """Quiz converting words to major numeric equivalent"""
    basic_quiz(use_letters=letters, use_naive=naive)


@quiz.command()
def cards():
    """Show a random card"""
    random_card()


@quiz.command()
@click.option("--config-file", type=str, default="~/.artofmemory.conf")
def pao(config_file):
    """Test out your Person Action Object (PAO) knowledge

    It supports just testing your PAO + shuffling them up to test combos
    """
    # config = get_artofmemory_config(config_file)

    fname = os.path.expanduser(config_file)
    if not os.path.exists(fname):
        click.error("Unable to read config file: {}".format(fname))
        return

    pao_quiz(fname)


@quiz.command("words")  # FIXME: ideally not grouped with "quiz"
@click.argument("numbers", nargs=-1)
def major_system_words(numbers):
    """Print out a possible words that match given number(s)."""
    print_number_words(numbers)


if __name__ == "__main__":
    quiz()
