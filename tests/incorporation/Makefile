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

GIT_URL ?= https://github.com/usnistgov/swid-autotools.git

srcdir := $(shell pwd)
top_srcdir := $(shell cd ../.. ; pwd)

all: \
  by_copying.swidtag \
  by_git_submodule.swidtag

.PHONY: \
  check-copying \
  check-git-submodule

by_copying.swidtag: \
  $(top_srcdir)/.git_ls_tree__sample.txt \
  library_files.txt \
  patched_files.txt
	rm -rf by_copying
	# Initialize from sample_nop source tree.
	rsync \
	  --files-from=$(top_srcdir)/.git_ls_tree__sample.txt \
	  --progress \
	  -av \
	  ../sample_nop/ \
	  by_copying/
	# Copy SWID files.
	rsync \
	  --files-from=library_files.txt \
	  --progress \
	  -av \
	  $(top_srcdir)/ \
	  by_copying/
	# Patch files to incorporate SWID support.
	rsync \
	  --files-from=patched_files.txt \
	  --progress \
	  -av \
	  ../sample_nop_corpus_tag/base/ \
	  by_copying/
	# Run build test.
	cd by_copying ; ./autogen.sh
	cd by_copying ; ./configure
	$(MAKE) -C by_copying PYTHON=$(PYTHON) check
	$(MAKE) -C by_copying PYTHON=$(PYTHON) installcheck
	$(MAKE) -C by_copying PYTHON=$(PYTHON) distcheck
	tar \
	  -xOzf \
	  by_copying/sample_nop-0.0.1.tar.gz \
	  sample_nop-0.0.1/swidtag/sample_nop.swidtag \
	  > _$@
	mv _$@ $@

by_git_submodule.swidtag: \
  $(top_srcdir)/.git_ls_tree__sample.txt \
  library_files.txt \
  patched_files.txt
	rm -rf by_git_submodule
	# Initialize from sample_nop source tree.
	rsync \
	  --files-from=$(top_srcdir)/.git_ls_tree__sample.txt \
	  --progress \
	  -av \
	  ../sample_nop/ \
	  by_git_submodule/
	# Treat this directory as its own independent Git repository, and track the SWID-autotools repository as a Git submodule.
	cd by_git_submodule ; \
	  git init .
	cd by_git_submodule ; \
	  git submodule add \
	    $(GIT_URL) \
	    deps/swid-autotools
	while read path ; do \
	  subdir=by_git_submodule/$$(dirname $$path); \
	  mkdir -p $$subdir ; \
	  pushd $$subdir ; \
	    ln -s \
	      ../deps/swid-autotools/$$path \
	      $$(basename $$path) ; \
	  popd ; \
	done < library_files.txt
	# Patch files to incorporate SWID support.
	rsync \
	  --files-from=patched_files.txt \
	  --progress \
	  -av \
	  ../sample_nop_corpus_tag/base/ \
	  by_git_submodule/
	# Run build test.
	cd by_git_submodule ; ./autogen.sh
	cd by_git_submodule ; ./configure
	$(MAKE) -C by_git_submodule PYTHON=$(PYTHON) check
	$(MAKE) -C by_git_submodule PYTHON=$(PYTHON) installcheck
	$(MAKE) -C by_git_submodule PYTHON=$(PYTHON) distcheck
	tar \
	  -xOzf \
	  by_git_submodule/sample_nop-0.0.1.tar.gz \
	  sample_nop-0.0.1/swidtag/sample_nop.swidtag \
	  > _$@
	mv _$@ $@

check: \
  by_copying.swidtag \
  by_git_submodule.swidtag

check-copying: \
  by_copying.swidtag

check-git-submodule: \
  by_git_submodule.swidtag

clean:
	rm -rf *.swidtag by_copying by_git_submodule
