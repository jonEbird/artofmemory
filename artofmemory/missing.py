"""Quiz what is missing."""

import os
import random
from typing import List

from .terminal import LineRepeater


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
            term.write("%2d/%d: %s" % (n, total, item))

        if talk:
            say("Okay, what is missing?")
        ans = input("What is missing? ")
        if ans.lower() == last_item.lower():
            print("Well done!")
        else:
            print("Sorry, it was '%s'." % last_item)
    except KeyboardInterrupt:
        print("\nOkay, we can quiz another time.")
