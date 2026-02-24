.PHONY: help install setup test lint format clean run-producer run-consumer run-dashboard

help:
	@echo "Crypto Streaming Pipeline - Available Commands"
	@echo "=============================================="
	@echo "make install      - Install dependencies"
	@echo "make setup        - Run setup script"
	@echo "make test         - Run tests"
	@echo "make lint         - Run linters"
	@echo "make format       - Format code"
	@echo "make clean        - Clean temporary files"
	@echo "make run-producer - Start producer"
	@echo "make run-consumer - Start consumer"
	@echo "make run-dashboard - Start dashboard"

install:
	pip install --upgrade pip
	pip install -r requirements.txt

setup:
	./setup.sh

test:
	pytest tests/ -v --cov=src --cov-report=term-missing

lint:
	flake8 src/ tests/
	black --check src/ tests/

format:
	black src/ tests/
	isort src/ tests/

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .pytest_cache .coverage htmlcov/

run-producer:
	cd src && python producer.py

run-consumer:
	cd src && python consumer.py

run-dashboard:
	streamlit run src/dashboard.py
