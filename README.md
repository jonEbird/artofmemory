# artofmemory
A tool to help practice memorization techniques such as using People Action Object (POA) techniques

# Getting started

    sudo yum install -y python3 python-virtualenvwrapper
    mkvirtualenv -v /usr/bin/python3
    pip install -r requirements.txt  # requirements-test.txt if planning to run tests

    python3 artofmemory.py

# Examples

    python3 artofmemory.py --cards
    python3 artofmemory.py --major-system

# Development

When setting up your environment, use the `requirements-test.txt` file for installing requirements.

Recommended way to execute tests:

    make test
