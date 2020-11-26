# Art of Memory

A tool to help practice memorization techniques such as using People Action Object (PAO) techniques.

# Getting started

See the [Environment Setup](CONTRIBUTING.md) section of the contributing guide for setup.
Then try executing `play.py`:

    ./play.py

You will also need to setup a `.artofmemory.conf` file in your home directory or in this
local directory. Its contents only requires a `[pao]` section consisting of numbers -to->
pao label. Basically this can be any values that you wish to be quizzed upon.

Here is a starter example:

    [pao]
    23 = Michael Jordan, shooting, basketball
    16 = Molly Ringwald, blowing candles, cake

# Examples

    ./play.py --cards
    ./play.py --major-system

Find a list of words that match the number `903` and `42`:

    ./play.py words 903 42
