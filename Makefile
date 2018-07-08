.PHONY: all, install, test, doc, clean, docker

all:
	make install
	make test
	#make doc
	#make docker

install:
	pip3 install -r requirements.txt
	python3 setup.py sdist
	pip3 install dist/boom-0.1.tar.gz

docker:
	docker build -t boom/docker .

test:
	py.test -v --color=yes tests

doc:
	doxygen Doxyfile

clean:
	rm -r dist

uninstall:
	pip3 uninstall boom -y
