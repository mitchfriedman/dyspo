.PHONY: build

nopyc:
	find . -name '*.pyc' | xargs rm -f || true

test: nopyc
	. venv/bin/activate; \
	python -m unittest

venv:
	virtualenv --python=python3 venv

clean:
	rm -rf venv

install: venv
	. venv/bin/activate; \
	pip install -r requirements.txt

build:
	python setup.py sdist bdist_wheel
