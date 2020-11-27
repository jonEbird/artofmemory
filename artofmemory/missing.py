"""Quiz what is missing."""

import os
import random
import textwrap
from typing import List

from .terminal import LineRepeater
from .data import bible


def explain() -> str:
    """Explain Person Action Object"""
    return textwrap.dedent(
        """\
        Missing game.

        If you have an existing memory system for memorizing a series of information, then
        you can try quizzing yourself when one of them are missing.

        One way of doing this is to apply a particular attribute to the item in your
        memory. Lets say you had a memory palace with all of the items in their proper
        locations. When you see or hear the item, image that it is then on fire. You need
        to really picture it burning. At the end, when you're asked which value is
        missing, you traverse your memory palace until you find an item which is not on
        fire. That is the answer.
        """
    )


def say(phrase, voice="Tessa"):
    """Say the phrase out loud."""
    # TODO: Support more platforms than just MacOS
    if os.uname()[0] == "Darwin":
        os.system("say -v %s %s" % (voice, phrase))


def quiz_missing(items: List[str], talk=False):
    """Leaving one out, print rest in random order, then ask for what is missing."""
    try:
        shuffled = items[:]
        random.shuffle(shuffled)

        total = len(shuffled)
        last_item = shuffled.pop()
        term = LineRepeater()
        for n, item in enumerate(shuffled):
            if talk:
                say(item)
            term.write(f"{n:2}/{total}: {item}")

        if talk:
            say("Okay, what is missing?")
        ans = input("What is missing? ")
        if ans.lower() == last_item.lower():
            print("Well done!")
        else:
            print(f"Sorry, it was '{last_item}'")
    except (EOFError, KeyboardInterrupt):
        print("\nOkay, we can quiz another time.")


def quiz_bible_books(talk: bool = False):
    """Try to identify the missing book of the Bible."""
    quiz_missing(bible.old_testament + bible.new_testament, talk=talk)
