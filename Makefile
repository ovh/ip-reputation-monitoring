CD=cd
FIND=find
DEL=rm
PYTHON=python
PIP=pip
COVERAGE=coverage
COVERALLS=coveralls
PYLINT=pylint
SPHINX=sphinx-build

MODULE_DIR=reputation
DOC_DIR=doc/build

clean: clean-doc
	$(FIND) . -name *.pyc | xargs $(DEL)

clean-doc:
	$(DEL) -rf $(DOC_DIR)

install-deps:
	$(PIP) install -r requirements.txt

install-dev-deps:
	$(PIP) install -r requirements/dev.txt

test: 
	cd $(MODULE_DIR) && \
	$(COVERAGE) > /dev/null 2>&1 && \
	$(COVERAGE) run --source='.' -m unittest discover && \
	$(COVERAGE) report \
		|| \
	$(PYTHON) -m unittest discover

coveralls:
	$(COVERAGE) erase && \
	cd $(MODULE_DIR) && \
	$(COVERAGE) > /dev/null 2>&1 && \
	$(COVERAGE) run --source='.' -m unittest discover && \
	$(COVERALLS)

lint:
	cd $(MODULE_DIR) && \
	$(PYLINT) --disable=W0141 --max-line-length=150 adapters/ api/ archive/ config/ default/ factory/ main.py mongo/ parsing/ reporting/ run_api.py tests/ spamhaus_monitor.py  tools/ utils/

doc: clean-doc
	$(SPHINX) -b html doc/source doc/build
