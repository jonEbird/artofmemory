lint:
	flake8

test: lint
	pytest

coverage: test
	open htmlcov/index.html
