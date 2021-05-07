README.rst: README.md
	pandoc --from=markdown --to=rst $< > $@

test:
	python src/braceexpand/__init__.py
	python test_braceexpand.py

.PHONY: test
