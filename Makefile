.PHONY: help install test run clean setup

help:
	@echo "Rearc Data Quest - Available Commands"
	@echo "======================================"
	@echo "make setup      - Set up virtual environment and install dependencies"
	@echo "make install    - Install dependencies"
	@echo "make run        - Run the complete data pipeline"
	@echo "make test       - Run all tests"
	@echo "make clean      - Clean up generated files and cache"
	@echo "make fetch      - Fetch data from BLS API"
	@echo "make process    - Process the latest fetched data"
	@echo "make analyze    - Analyze the latest processed data"

setup:
	python3 -m venv venv
	@echo "Virtual environment created. Activate with: source venv/bin/activate"

install:
	pip install --upgrade pip
	pip install -r requirements.txt

run:
	./run_pipeline.sh

test:
	python3 -m pytest tests/ -v

fetch:
	python3 scripts/fetch_data.py

process:
	python3 scripts/process_data.py

analyze:
	python3 scripts/analyze_data.py

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	rm -rf .pytest_cache
	@echo "Cleaned up cache files"
