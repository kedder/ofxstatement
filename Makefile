VENV=$(abspath .venv)
PIP=$(VENV)/bin/pip

all: bin/ofxstatement bin/pytest

$(VENV):
	python3 -m venv $(VENV)

bin:
	mkdir $@

bin/ofxstatement: $(VENV)/bin/ofxstatement | bin
	ln -sf $(VENV)/bin/ofxstatement $@
	touch $@

bin/pytest: $(VENV)/bin/ofxstatement | bin
	ln -sf $(VENV)/bin/pytest $@
	touch $@

$(VENV)/bin/ofxstatement: $(VENV) setup.py
	$(PIP) install --editable .[test]

PHONY: test
test: bin/pytest
	bin/pytest

PHONY: coverage
coverage: bin/pytest
	./bin/pytest --cov src/ofxstatement
