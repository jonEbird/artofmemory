import random
import textwrap
from configparser import ConfigParser


def explain() -> str:
    """Explain Person Action Object"""
    return textwrap.dedent(
        """\
        Person Action Object (PAO)

        The PAO is a system of encoding where you attribute a specific Person with an
        Action that includes an Object. This is a composite object which you can then use
        in a variety of ways. The idea is that you develop a collection of PAOs and assign
        each of them a number.

        Examples:
        15: Albert Einstein (person) writing (action) on a blackboard (object).
        16: Molly Ringwald (person) blowing candles (action) on a cake (object).
        23: Michael Jordan (person) shooting (action) a basketball (object).

        Armed with such an inventory you can use it for encoding of other information. Say
        you want to memorize a series of numbers and you had a PAO inventory from
        00-99. You could then assign the first six digits with a special combination of
        your PAO collection.

        Example:
        162315 => Molly Ringwald shooting a blackboard

        By doing this, you're compressing six digits into a single, composite image.
            """
    )


def flatten_pao(d):
    """Yield back (num, item) tuples for each PAO broken into items.

    The PAO item will be prefixed with either 'p:', 'a:', 'o:' to help denote its part of
    the overall PAO.

    Args:
        d (dict): dictionary-like object that supports .items()
    Yields:
        (str, str)
    """
    for num, pao in d.items():
        person, action, obj = pao.split(",")
        yield (num, "p:" + person.strip())
        yield (num, "a:" + action.strip())
        yield (num, "o:" + obj.strip())


def basic_quiz(config_file: str):
    """Test out your Person Action Object (PAO) knowledge

    It supports just testing your PAO + shuffling them up to test combos
    """
    config = ConfigParser()
    config.read(config_file)

    # TODO -- add an option to limit the values to test
    # e.g. if I only want to test PAO for 1 through 4

    # TODO add support for properly mixing up the PAO and testing
    if "pao" not in config.sections():
        print("No PAO Config setup.  See README")
        return

    # Randomize the PAO items
    pao_pairs = list(flatten_pao(config["pao"]))
    random.shuffle(pao_pairs)

    correct = 0
    total = 0
    for number, item in pao_pairs:
        try:
            guess = input("{}\n=> ".format(item))
        except (EOFError, KeyboardInterrupt):
            break
        if not guess:
            continue

        if guess == number:
            print("CORRECT!")
            correct += 1
        else:
            print("INCORRECT: {}".format(number))
        total += 1

    if total:
        print("\n{:>2}% Correct".format(correct / float(total) * 100))
