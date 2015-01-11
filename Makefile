README.rst: README.mkd
	pandoc --from=markdown --to=rst $< > $@

test:
	python braceexpand.py
	python test_braceexpand.py

.PHONY: test
