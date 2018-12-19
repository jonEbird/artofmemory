# artofmemory
A tool to help practice memorization techniques such as using People Action Object (PAO) techniques

# Getting started

    sudo yum install -y python3 python-virtualenvwrapper
    mkvirtualenv -v /usr/bin/python3
    pip install -r requirements.txt  # requirements-test.txt if planning to run tests

    python3 artofmemory.py

You will also need to setup a `.artofmemory.conf` file in your home directory or in this
local directory. Its contents only requires a `[pao]` section consisting of numbers -to->
pao label. Basically this can be any values that you wish to be quizzed upon.

Here is a starter example:

    [pao]
    23 = Michael Jordan, shooting, basketball
    16 = Molly Ringwald, blowing candles, cake

# Examples

    python3 artofmemory.py --cards
    python3 artofmemory.py --major-system

# Development

When setting up your environment, use the `requirements-test.txt` file for installing requirements.

Recommended way to execute tests:

    make test
