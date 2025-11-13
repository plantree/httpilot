.PHONY: help install run test clean dev version tag

# Default target
help:
	@echo "HTTPilot - HTTP Testing Tool"
	@echo ""
	@echo "Available commands:"
	@echo "  help     - Show this help message"
	@echo "  install  - Install dependencies"
	@echo "  dev      - Install development dependencies"
	@echo "  run      - Run the application in development mode"
	@echo "  test     - Run basic tests"
	@echo "  test-all - Run comprehensive test suite"
	@echo "  test-unit - Run unit tests only"
	@echo "  test-integration - Run integration tests only"
	@echo "  coverage - Run tests with coverage report"
	@echo "  test-report - Generate detailed test reports"
	@echo "  clean    - Clean up cache files"
	@echo "  format   - Format code with black (if installed)"
	@echo "  lint     - Run code linting"
	@echo "  version  - Show current version"
	@echo "  tag      - Create a new release tag (usage: make tag VERSION=x.y.z)"

# Install dependencies
install:
	pip install -r requirements.txt

# Install development dependencies
dev: install
	pip install pytest pytest-cov black flake8

build: install
	pip install .

# Run the application
run:
	python run.py

# Run basic tests
test:
	pytest tests/ -v

# Run comprehensive test suite
test-all:
	python run_tests.py

# Run unit tests only (exclude integration tests)
test-unit:
	pytest tests/ -v -k "not integration"

# Run integration tests only
test-integration:
	pytest tests/test_integration.py -v

# Run tests with coverage
coverage:
	pytest tests/ --cov=src --cov-report=html --cov-report=term-missing --cov-report=xml

# Generate detailed test reports
test-report:
	pytest tests/ --cov=src --cov-report=html --cov-report=xml --junit-xml=test-results.xml -v

# Run code linting
lint:
	flake8 src/ tests/ --max-line-length=100 --extend-ignore=E203,W503

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

# Show current version
version:
	@python -m setuptools_scm

# Create a new release tag
tag:
	@if [ -z "$(VERSION)" ]; then \
		echo "Error: VERSION is required. Usage: make tag VERSION=x.y.z"; \
		exit 1; \
	fi
	@echo "Creating tag v$(VERSION)..."
	@git tag -a v$(VERSION) -m "Release version $(VERSION)"
	@echo "Tag v$(VERSION) created successfully!"
	@echo "To push: git push origin v$(VERSION)"