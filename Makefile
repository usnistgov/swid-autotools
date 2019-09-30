#!/usr/bin/make -f

# This software was developed at the National Institute of Standards
# and Technology by employees of the Federal Government in the course
# of their official duties. Pursuant to title 17 Section 105 of the
# United States Code this software is not subject to copyright
# protection and is in the public domain. NIST assumes no
# responsibility whatsoever for its use by other parties, and makes
# no guarantees, expressed or implied, about its quality,
# reliability, or any other characteristic.
#
# We would appreciate acknowledgement if the software is used.

SHELL := /bin/bash

PYTHON ?= python

all:
	@echo "Run 'make check' to run unit tests."
	@echo "Run 'make check-swidval' to run swidval unit tests.  (Requires Java.  May require non-automated download.)"
	@echo "Run 'make check-incorporation' to run incorporation unit tests.  (Requires networking.)"
	@echo "Run 'make explain' to see differences neded to start SWID tag implementation."
	@echo "Run 'make docs' to confirm generated documentation files are up to date.  ('make clean' or 'make clean-docs' will remove generated files.)"

.PHONY: \
  check-docs \
  check-docs-README \
  check-docs-TUTORIAL \
  check-incorporation \
  check-swidval \
  clean-docs \
  docs \
  explain

.git_ls_tree__sample.txt:
	@test -r .git/HEAD || (echo "ERROR:Makefile:This target can only be made from a Git clone." >&2 ; exit 2)
	git ls-tree \
	  --name-only \
	  -r \
	  HEAD \
	  -- \
	  tests/sample_nop \
	  | sed \
	    -e 's@tests/sample_nop/@@' \
	    | sort \
	    > _$@
	mv _$@ $@

.git_ls_tree__sample_tagged.txt:
	@test -r .git/HEAD || (echo "ERROR:Makefile:This target can only be made from a Git clone." >&2 ; exit 2)
	git ls-tree \
	  --name-only \
	  -r \
	  HEAD \
	  -- \
	  tests/sample_nop_corpus_tag/base \
	  | sed \
	    -e 's@tests/sample_nop_corpus_tag/base/@@' \
	    | sort \
	      > _$@
	mv _$@ $@

# BSD sed file replacements c/o:
#   https://stackoverflow.com/a/34070185
# This answer works if using GNU sed:
#   https://stackoverflow.com/a/6790967
README.md: \
  .README.md.in \
  Makefile
	rm -f _$@ __$@ ___$@
	cp .README.md.in _$@
	$(MAKE) --silent > ___$@
	sed \
	  -e '/@MAKE_ALL@/r ___$@' \
	  -e '/@MAKE_ALL@/d' \
	  _$@ \
	  > __$@
	mv __$@ _$@
	rm ___$@
	mv _$@ $@

TUTORIAL.md: \
  .TUTORIAL.md.in \
  .git_ls_tree__sample.txt \
  .git_ls_tree__sample_tagged.txt \
  Makefile \
  tests/incorporation/library_files.txt \
  tests/incorporation/patched_files.txt \
  tests/sample_nop/src/nop.c
	rm -f _$@ __$@ ___$@
	cp .TUTORIAL.md.in _$@
	$(MAKE) explain > /dev/null #Prevent dependency build artifacts from entering documentation
	$(MAKE) --no-print-directory explain > ___$@
	sed \
	  -e '/@MAKE_EXPLAIN@/r ___$@' \
	  -e '/@MAKE_EXPLAIN@/d' \
	  _$@ \
	  > __$@
	mv __$@ _$@
	tail -n3 tests/sample_nop/src/nop.c > ___$@
	sed \
	  -e '/@NOP_C@/r ___$@' \
	  -e '/@NOP_C@/d' \
	  _$@ \
	  > __$@
	mv __$@ _$@
	cat tests/incorporation/library_files.txt > ___$@
	sed \
	  -e '/@LIBRARY_FILES_TXT@/r ___$@' \
	  -e '/@LIBRARY_FILES_TXT@/d' \
	  _$@ \
	  > __$@
	mv __$@ _$@
	cat tests/incorporation/patched_files.txt > ___$@
	sed \
	  -e '/@PATCHED_FILES_TXT@/r ___$@' \
	  -e '/@PATCHED_FILES_TXT@/d' \
	  _$@ \
	  > __$@
	mv __$@ _$@
	while read x; do \
	  echo ln -s deps/swid-autotools/$$x $$x ; \
	  echo git add $$x ; \
	done \
	  < tests/incorporation/library_files.txt \
	  > ___$@
	sed \
	  -e '/@GIT_SUBMOD_LN_S@/r ___$@' \
	  -e '/@GIT_SUBMOD_LN_S@/d' \
	  _$@ \
	  > __$@
	mv __$@ _$@
	rm ___$@
	mv _$@ $@

check:
	$(MAKE) -C tests PYTHON=$(PYTHON) check

check-docs: \
  check-docs-README \
  check-docs-TUTORIAL

# This target can only be run from a Git checkout.
check-docs-README: \
  README.md
	@if [ -r .git/HEAD ]; then \
	  if [ 0 -ne $$(git diff README.md | wc -l) ]; then \
	    echo "ERROR:Makefile:README.md has changed since its last tracked refresh." >&2 ; \
	    git diff README.md ; \
	    exit 1 ; \
	  fi ; \
	else \
	  echo "INFO:Makefile:README.md can only be checked from a Git repository." ; \
	fi

# This target can only be run from a Git checkout.
check-docs-TUTORIAL: \
  TUTORIAL.md
	@if [ -r .git/HEAD ]; then \
	  if [ 0 -ne $$(git diff TUTORIAL.md | wc -l) ]; then \
	    echo "ERROR:Makefile:TUTORIAL.md has changed since its last tracked refresh." >&2 ; \
	    git diff TUTORIAL.md ; \
	    exit 1 ; \
	  fi ; \
	else \
	  echo "INFO:Makefile:TUTORIAL.md can only be checked from a Git repository." ; \
	fi

check-incorporation: \
  .git_ls_tree__sample.txt \
  check
	$(MAKE) -C tests PYTHON=$(PYTHON) check-incorporation

check-swidval: \
  check
	$(MAKE) -C tests PYTHON=$(PYTHON) check-swidval

clean:
	$(MAKE) clean-docs
	$(MAKE) -C tests clean

# The rm guarded by .git/HEAD presence is for restoring files that need to be generated from a Git clone of this repository.  'make docs' otherwise couldn't be reliably regenerated, as build artifacts might accidentally be incorporated.
clean-docs:
	if [ -r .git/HEAD ]; then rm -f .git_ls_tree__sample.txt .git_ls_tree__sample_tagged.txt ; fi
	rm -f README.md TUTORIAL.md

docs: \
  README.md \
  TUTORIAL.md

# The "|| true" following diff is due to diff exiting non-0 on finding any differences.
explain: \
  .git_ls_tree__sample.txt \
  .git_ls_tree__sample_tagged.txt
	@echo "These are the changes to configure.ac and Makefile.am needed to add SWID tags (noting that the NIST reference should be replaced with the implementing organization's authorship information):"
	@echo
	diff tests/sample_nop/configure.ac tests/sample_nop_corpus_tag/base/configure.ac || true
	diff tests/sample_nop/Makefile.am tests/sample_nop_corpus_tag/base/Makefile.am || true
	@echo
	@echo "Note the lib/ and include/ directories also have support files soft-linked in and referenced by their Makefile.am files."
	@echo
	@comm \
	  -13 \
	  .git_ls_tree__sample.txt \
	  .git_ls_tree__sample_tagged.txt \
	  | grep -v Makefile.am
	@echo
	@echo "Those files can be copied into the source tree if soft-links and Git submodule tracking are not desired."
	@echo
	@echo "Last, note that the soft-linked files are added to EXTRA_DIST."
	@echo
	grep EXTRA_DIST tests/sample_nop_corpus_tag/base/{include,lib}/Makefile.am
