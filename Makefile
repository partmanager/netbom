up:
	sudo docker compose up netbom_backend
.PHONY: up

build:
	sudo docker compose up --build netbom_backend
.PHONY: build

clean:
	sudo docker compose down -v
.PHONY: clean

terminal:
	sudo docker exec -it netbom_backend bash
.PHONY: terminal

docs:
	make uml
	make tests
	sphinx-build -M html docs/ docs/_build/
.PHONY: docs

uml:
	mkdir -p docs/uml
	pyreverse src/netbom -d docs/uml
	dot -Tsvg docs/uml/packages.dot -o docs/uml/packages.svg
	dot -Tsvg docs/uml/classes.dot -o docs/uml/classes.svg
.PHONY: uml

doctests:
	python -m doctest -v docs/index.rst docs/netlist.rst docs/netlist_readers.rst
.PHONY: doctests

unittests:
	python tests/test_bom.py
	python tests/test_bom_readers.py
	python tests/test_netlist.py
	python tests/test_netlist_readers.py
.PHONY: unittests

tests:
	make unittests
	make doctests
.PHONY: tests

lint:
	pylint netbom/netlist.py
.PHONY: lint

versions:
	python --version
	pip freeze
.PHONY: versions

freeze:
	pip freeze > requirements.txt
.PHONY: freeze
