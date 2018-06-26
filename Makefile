.PHONY: all, install, test, doc, clean

all:
	make install
	make test
	#make doc

install:
	pip3 install -r requirements.txt
	python3 setup.py sdist
	pip3 install dist/boom-0.1.tar.gz

test:
	py.test -v --color=yes tests

doc:
	doxygen Doxyfile

clean:
	rm -r dist

uninstall:
	pip3 uninstall boom -y
