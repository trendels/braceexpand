test:
	python braceexpand.py
	python test_braceexpand.py

README.rst: README.mkd
	pandoc --from=markdown --to=rst $< > $@
