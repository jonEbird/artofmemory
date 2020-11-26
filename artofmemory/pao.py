import random
from configparser import ConfigParser


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


def pao_quiz(config_file: str):
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

    pao_pairs = list(flatten_pao(config["pao"]))

    correct = 0
    total = 0
    try:
        while True:
            # Randomize the PAO items
            random.shuffle(pao_pairs)

            for number, item in pao_pairs:
                guess = input("{}\n=> ".format(item))
                if not guess:
                    continue
                if guess == number:
                    print("CORRECT!")
                    correct += 1
                else:
                    print("INCORRECT: {}".format(number))
                total += 1
    except KeyboardInterrupt:
        if total:
            print("\n{:>2}% Correct".format(correct / float(total) * 100))
