# Art of Memory

A tool to help practice memorization techniques such as using People Action Object (PAO) techniques.

# Getting started

See the [Environment Setup](CONTRIBUTING.md) section of the contributing guide for setup.
Then try executing `aom.py`:

    ./aom.py

There are different sub-commands or topics that can be covered.
Each section should support a `--explain` option that helps the particular topic.

## Person Place Object (PAO)

Support PAO quizzing.
For this you will need to setup a `.artofmemory.conf` file in your home directory.
Its contents only requires a `[pao]` section consisting of numbers -to-> pao label.
Basically this can be any values that you wish to be quizzed upon.

Here is a starter example:

    [pao]
    23 = Michael Jordan, shooting, basketball
    16 = Molly Ringwald, blowing candles, cake

Then try quizzing yourself:

    ./aom.py pao --explain --quiz

## Number / Word Major System

Support for both identifying / processing words or numbers as well as quizzing yourself.

Quiz yourself with the system while explaining how the system works:

    ./aom.py --explain --quiz

Find a list of words that match the number `903` and `42`:

    ./aom.py words 903 42

Or get a rather large summary page with numbers from 00 to 99:

    ./aom.py words --summary > words.txt

See how you might encode a message into numbers:

    ./aom.py words such great words

## Missing word

Play a little game to see if you can keep track of which word is missing.
There are a few pre-built categories such as the books of the Bible.

Try quizzing yourself to see which book of the Bible is missing:

    ./aom.py missing --bible

Or pass in your own choices:

    ./aom.py missing --bible apple orange pear cherry banana

## Cards

For now this is a bit of a stub.
Can only print out a random card for now.
