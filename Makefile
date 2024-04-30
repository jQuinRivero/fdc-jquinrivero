lint:
	poetry run flake8 src/ tests/

run-main:
	poetry run python -m src.fig_data_challenge.main

setup:
	poetry install
	poetry run pre-commit install

test:
	poetry run pytest
