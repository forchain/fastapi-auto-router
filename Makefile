.PHONY: install test lint clean build publish build-uv publish-uv

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

# Traditional pip-based build and publish
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

# UV-based build and publish (recommended)
build-uv: clean
	uv build

publish-uv: build-uv
	uv publish

publish-test-uv: build-uv
	uv publish --repository testpypi