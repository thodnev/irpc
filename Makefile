# These variables could be set from the cmdline, and also from the env for the first two.
PKGNAME		  ?= irpc
SPHINXOPTS    ?=
DOCSRCDIR	  := docs
DOCBUILDDIR   := $(DOCSRCDIR)/_build

.PHONY: _default doc-api doc clean tidy build-clean build-dev build-source build-wheel test docs

# This target is run if no arguments are provided to make
_default: build

doc-clean: $(DOCSRCDIR)
	sphinx-build -M clean "$(DOCSRCDIR)" "$(DOCBUILDDIR)" $(SPHINXOPTS)
	rm -rf "$(DOCSRCDIR)/api"

doc-api: $(DOCSRCDIR)
	sphinx-apidoc -T -o "$(DOCSRCDIR)/api" $(PKGNAME) $(SPHINXOPTS)

# Sphinx catch-all target: route all docs-... targets to Sphinx using the "make mode" option.
doc-%: $(DOCSRCDIR)
	sphinx-build -M $(subst doc-,,$@) "$(DOCSRCDIR)" "$(DOCBUILDDIR)" $(SPHINXOPTS)

doc: doc-clean doc-api doc-html



build-clean:
	python3 ./setup.py clean --all

build-dev:
	USE_LINE_TRACE=1 python3 ./setup.py build_ext --inplace

build-source:
	python3 ./setup.py sdist

build-wheel:
	python3 ./setup.py bdist_wheel

build: | build-clean build-source build-wheel


test:
	python3 -m pytest tests --cov=$(PKGNAME)

clean:
	rm -rf *.egg-info build

tidy: clean
	rm -rf dist
