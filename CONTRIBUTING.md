# Contributing

Please be considerate to others when contributing or helping.
For an addition to be accepted, create a pull request to the repository for consideration.
Ideally adding test coverage for the fix / new feature you are adding.

# Environment Setup

This project uses Python and is best if we are all using the same revision of Python.
Recommended to use [pyenv][] for managing the copies of Python on your system.
The local `.python-version` specifies the current version.

It is highly recommended to setup a virtualenv for local development.
To aid the preparation of the venv, there is a local `.envrc` file which is used by [direnv][] but you can manually source the file.
It will create the venv while using the correct Python.

Once you have the correct version of Python and have an activated venv, time to install requirements:

    pip install -r requirements.txt  # requirements-test.txt if planning to run tests

# Testing

We use [pytest][] for running the tests.
You can either run it directly or use the Makefile to execute the tests which will also run linting:

    make test

It is configured to provide coverage for the code as well.
To view the coverage report, run:

    make coverage


[pyenv]: https://github.com/pyenv/pyenv
[direnv]: https://github.com/direnv/direnv
[pytest]: https://docs.pytest.org/en/stable/
[flake8]: https://flake8.pycqa.org/en/latest/
[black]: https://github.com/psf/black
[black-setup]: https://github.com/psf/black/blob/master/docs/editor_integration.md#other-editors
