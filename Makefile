.PHONY: test cleantest

export PYTHONPATH := ./:$(PYTHONPATH)


test:
	py.test --verbose --color=yes tests

doc:
	bash scripts/create_docs.sh
