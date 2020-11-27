#!/usr/bin/env python3

import sys
import tty
import termios


class LineRepeater(object):
    """Utility class to print a line to the terminal and then erase it again."""

    def __init__(self):
        self.__max_line = 0

    def get_key(self):
        # TODO: Figure out why this is not working... works within simply python
        # REPL. Either the REPL does something "good" for the tty or perhaps 'click'
        # module is interfering?
        #   Once fixed, you can remove next line
        return input()

        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

    def write(self, msg):
        line = msg
        if len(line) > self.__max_line:
            self.__max_line = len(line)
        else:
            # Erase prior max length with spaces
            print("{}{}".format(" " * self.__max_line, "\b" * self.__max_line), end="")
        print(line, end="")
        self.get_key()
        print("\b" * len(line), end="")
