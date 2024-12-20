.PHONY: install test lint clean build publish

install:
	pip install -e .

dev-install:
	pip install -r dev-requirements.txt

test:
	pytest tests/

lint:
	black src/ tests/
	flake8 src/ tests/

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +

build: clean
	pip install build
	python -m build

publish: build
	pip install twine
	twine check dist/*
	twine upload dist/*

publish-test: build
	pip install twine
	twine check dist/*
	twine upload --repository testpypi dist/*