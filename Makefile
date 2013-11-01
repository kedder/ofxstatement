all: bin/ofxstatement

.venv:
	virtualenv -p python3 --no-site-packages .venv

bin/buildout: .venv
	.venv/bin/python bootstrap.py

bin/ofxstatement: bin/buildout buildout.cfg setup.py
	./bin/buildout
	./bin/python setup.py develop
	touch bin/ofxstatement