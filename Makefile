.PHONY: install ingest chat clean help

help:
	@echo "Available commands:"
	@echo "  make install   Install all dependencies"
	@echo "  make ingest    Load and embed documents from data/"
	@echo "  make chat      Start interactive RAG CLI"
	@echo "  make clean     Remove vectorstore and pycache"

install:
	pip install --upgrade pip
	pip install -e ".[dev]"

ingest:
	python -m rag_pipeline.ingest

chat:
	python -m rag_pipeline.app

clean:
	rm -rf vectorstore/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -name "*.pyc" -delete
