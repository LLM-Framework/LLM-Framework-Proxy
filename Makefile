.PHONY: run install test

install:
	pip install -r requirements.txt

run:
	uvicorn src.main:app --host 0.0.0.0 --port 8002 --reload

test:
	pytest tests/ -v