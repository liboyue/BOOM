.PHONY: all, install, test, doc, clean, docker

all:
	make install
	make test
	make doc
	make docker

install:
	pip install -r requirements.txt
	python setup.py sdist
	pip install dist/boom-0.1.tar.gz

docker:
	docker build -t boom/docker .

test:
	cd tests && py.test -v --color=yes . && cd ..

doc:
	doxygen Doxyfile

clean:
	rm -r dist

uninstall:
	pip uninstall boom -y
