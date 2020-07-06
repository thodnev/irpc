.PHONY: _default clean tidy build-clean build-dev build-source build-wheel test

_default: build

build-clean:
	./setup.py clean --all

build-dev:
	USE_LINE_TRACE=1 ./setup.py build_ext --inplace

build-source:
	./setup.py sdist

build-wheel:
	./setup.py bdist_wheel

build: | build-clean build-source build-wheel

test:
	pytest tests --cov=xrpc

clean:
	rm -rf *.egg-info build

tidy: clean
	rm -rf dist
