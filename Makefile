nopyc:
	find . -name '*.pyc' | xargs rm -f || true

test: nopyc
	. venv/bin/activate; \
	python tests/__init__.py

venv:
	virtualenv --python=python3 venv

clean:
	rm -rf venv

install: venv
	. venv/bin/activate; \
	pip install -r requirements.txt
