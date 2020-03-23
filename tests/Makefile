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

top_srcdir := $(shell cd .. ; pwd)

SWIDVAL_ZIP ?= $(top_srcdir)/tests/share/swidval-0.5.0-swidval.zip

PYTHON ?= python

AUTOTOOL_SUPPORT_FILES := \
  $(top_srcdir)/include/swid.am \
  $(top_srcdir)/lib/swidtag.py \
  $(top_srcdir)/m4/swid.m4

all:

.PHONY: \
  check-incorporation \
  check-swidval

$(SWIDVAL_ZIP):
	$(MAKE) -C share
	test -r $@

check: \
  sample_nop_corpus_tag.check.done.log

check-incorporation: \
  sample_nop_corpus_tag.check.done.log
	$(MAKE) -C incorporation PYTHON=$(PYTHON)

check-swidval: \
  $(SWIDVAL_ZIP) \
  sample_nop_corpus_tag.check.done.log
	$(MAKE) -C sample_nop_corpus_tag PYTHON=$(PYTHON) check-swidval

# Clean in reverse-build-dependency order.
clean: \
  clean-incorporation \
  clean-sample_nop_corpus_tag \
  clean-sample_nop

clean-incorporation:
	$(MAKE) -C incorporation clean

clean-sample_nop:
	rm -f sample_nop.distcheck.done.log
	cd sample_nop ; test ! -r Makefile || make distclean || true

clean-sample_nop_corpus_tag:
	rm -f sample_nop_corpus_tag.check.done.log
	$(MAKE) -C sample_nop_corpus_tag clean

sample_nop.distcheck.done.log:
	$(MAKE) clean-sample_nop
	cd sample_nop ; ./autogen.sh
	cd sample_nop ; ./configure
	$(MAKE) -C sample_nop PYTHON=$(PYTHON) check
	$(MAKE) -C sample_nop PYTHON=$(PYTHON) installcheck
	$(MAKE) -C sample_nop PYTHON=$(PYTHON) distcheck
	touch sample_nop.distcheck.done.log

sample_nop_corpus_tag.check.done.log: \
  $(AUTOTOOL_SUPPORT_FILES) \
  sample_nop.distcheck.done.log
	$(MAKE) -C sample_nop_corpus_tag PYTHON=$(PYTHON) check
	touch $@
