#!/usr/bin/env python3

import os

import click

from lib.cards import random_card
from lib.major import basic_quiz
from lib.pao import pao_quiz


@click.command()
@click.option("--letters", is_flag=True)
def major_system(letters):
    """Quiz converting words to major numeric equivalent"""
    basic_quiz(use_letters=letters)


@click.command()
def cards():
    """Show a random card"""
    random_card()


@click.command()
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


@click.group()
def play():
    pass


play.add_command(cards)
play.add_command(major_system)
play.add_command(pao)


if __name__ == "__main__":
    play()
