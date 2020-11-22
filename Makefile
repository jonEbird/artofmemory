lint:
	flake8
	black --check .

test: lint
	pytest

coverage: test
	open htmlcov/index.html
