.PHONY: all, install, test, doc, clean, docker

PACKAGE_NAME=python
PACKAGE_VERSION=$(strip $(shell apt-cache policy $(PACKAGE_NAME) | grep Installed: | cut -d: -f2))
all:
	@echo "package name: $(PACKAGE_VERSION)"
	make install
	make test
	make doc
	make docker

install:
	pip install -r requirements.txt
	python setup.py sdist
	pip install dist/boom-0.1.tar.gz --user

docker:
	docker build -t boom/docker .

test:
	py.test -v --color=yes tests

doc:
	doxygen Doxyfile

clean:
	rm -r dist

uninstall:
	pip uninstall boom -y
