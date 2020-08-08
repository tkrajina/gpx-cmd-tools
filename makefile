GIT_PORCELAIN_STATUS=$(shell git status --porcelain)

.PHONY: mypy
mypy:
	mypy --strict .

.PHONY: help-all
help-all:
	./gpxclean -h
	./gpxinfo -h
	./gpxmerge -h
	./gpxsimplify -h
	./gpxsplitter -h

.PHONY: check-all-commited
check-all-commited:
	if [ -n "$(GIT_PORCELAIN_STATUS)" ]; \
	then \
	    echo 'YOU HAVE UNCOMMITED CHANGES'; \
	    git status; \
	    exit 1; \
	fi

.PHONY: pypi-upload
pypi-upload: clean mypy help-all check-all-commited
	rm -Rf dist/*
	python setup.py sdist
	twine upload dist/*

.PHONY: clean
clean:
	rm -Rf build
	rm -Rf dist
	rm -Rf MANIFEST
