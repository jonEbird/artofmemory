#!/usr/bin/env python3

import os

import click

from artofmemory.cards import random_card
from artofmemory.major import basic_quiz
from artofmemory.pao import pao_quiz


@click.group()
def quiz():
    pass


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


if __name__ == "__main__":
    quiz()
