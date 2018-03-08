.PHONY: all, install, test, doc

all:
	make install
	make test
	make doc

install:
	python setup.py install

test:
	py.test --verbose --color=yes tests

doc:
	bash scripts/create_docs.sh

