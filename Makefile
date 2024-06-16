test:
	pytest . --cov

lint:
	ruff check . --config pyproject.toml --fix

format:
	ruff format . --config pyproject.toml
