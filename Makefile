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

tests:
	python tests/test_bom.py
	python tests/test_bom_readers.py
	python tests/test_netlist.py
	python tests/test_netlist_readers.py
	python -m doctest -v docs/index.rst docs/netlist.rst docs/netlist_readers.rst
.PHONY: tests

lint:
	pylint netbom/netlist.py
.PHONY: lint

freeze:
	pip freeze > requirements.txt
.PHONY: freeze
