.PHONY: help install run test clean dev

# Default target
help:
	@echo "HTTPilot - HTTP Testing Tool"
	@echo ""
	@echo "Available commands:"
	@echo "  help     - Show this help message"
	@echo "  install  - Install dependencies"
	@echo "  dev      - Install development dependencies"
	@echo "  run      - Run the application in development mode"
	@echo "  test     - Run tests"
	@echo "  coverage - Run tests with coverage report"
	@echo "  clean    - Clean up cache files"
	@echo "  format   - Format code with black (if installed)"

# Install dependencies
install:
	pip install -r requirements.txt

# Install development dependencies
dev: install
	pip install pytest pytest-cov black flake8

# Run the application
run:
	python run.py

# Run tests
test:
	pytest

# Run tests with coverage
coverage:
	pytest --cov=src --cov-report=html --cov-report=term

# Clean up cache files
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf .pytest_cache/
	rm -rf src/__pycache__/

# Format code (requires black)
format:
	black src/ tests/ --line-length 88