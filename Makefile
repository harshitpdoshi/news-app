.PHONY: help install test coverage run clean

help:
	@echo "News App - CLI RSS Reader"
	@echo ""
	@echo "Usage:"
	@echo "  make install     Install dependencies"
	@echo "  make test        Run tests"
	@echo "  make coverage    Run tests with coverage report"
	@echo "  make run         Run the application"
	@echo "  make clean       Clean up generated files"

install:
	uv sync --extra test

test:
	uv run pytest news_app/tests/ -v

coverage:
	uv run pytest --cov=news_app --cov-report=term-missing

run:
	uv run python main.py

clean:
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf htmlcov
	rm -rf feeds.db