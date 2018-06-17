.PHONY: all, install, test, doc, clean

all:
	make install
	make test
	#make doc

install:
	pip install -r requirements.txt
	python setup.py sdist
	pip install dist/boom-0.1.tar.gz

test:
	py.test -v --color=yes tests

doc:
	doxygen Doxyfile

clean:
	rm -r dist

uninstall:
	pip uninstall boom -y
