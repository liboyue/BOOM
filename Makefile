.PHONY: all, install, test, doc

all:
	make install
	make test
	#make doc

install:
	pip install -r requirements.txt
	python setup.py install

test:
	py.test --verbose --color=yes tests

doc:
	doxygen Doxyfile
