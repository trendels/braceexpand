README.rst: README.md
	pandoc --from=markdown --to=rst $< > $@

init:
	pip install -e .

test:
	python src/braceexpand/__init__.py
	python test_braceexpand.py

.PHONY: test
