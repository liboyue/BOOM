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
	mkdir -p tests/data
	rabbitmq-server &
	mongod --dbpath tests/data --bind_ip 127.0.0.1 -logpath /tmp/mongod.log &
	sleep 5
	cd tests && py.test -v --color=yes . && cd ..
	rabbitmqctl stop
	killall mongod
	rm -rf tests/data

doc:
	doxygen Doxyfile

clean:
	rm -r dist

uninstall:
	pip uninstall boom -y
