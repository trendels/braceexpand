all: typecheck test README.rst

README.rst: README.md
	pandoc --from=markdown --to=rst $< > $@

init:
	pip install -e .

test:
	python src/braceexpand/__init__.py
	python test_braceexpand.py

typecheck:
	mypy --strict src/braceexpand/__init__.py

.PHONY: all test typecheck
