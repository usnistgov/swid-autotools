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

top_srcdir := $(shell cd ../.. ; pwd)

PYTHON ?= python

SWIDVAL_ZIP ?= $(top_srcdir)/tests/share/swidval-0.5.0-swidval.zip

AUTOTOOL_SUPPORT_FILES := \
  $(top_srcdir)/include/swid.am \
  $(top_srcdir)/lib/swidtag.py \
  $(top_srcdir)/m4/swid.m4

DIST_SWIDTAG_TARGETS := \
  dist-bzip2-swidtag \
  dist-gzip-swidtag \
  dist-lzip-swidtag \
  dist-xz-swidtag \
  dist-zip-swidtag

TEST_DIRNAMES := \
  base \
  configure_disable_swid_xmllint \
  lang \
  tagname \
  tagid_file \
  tagversion_file \
  versionscheme

CHECK_SWIDTAG_TARGETS := $(foreach test_dirname,$(TEST_DIRNAMES),check-swidtag-$(test_dirname))
CHECK_SWIDVAL_CORPUS_TARGETS := $(foreach test_dirname,$(TEST_DIRNAMES),check-swidval-corpus-$(test_dirname)/swidval-passes.log)
CHECK_SWIDVAL_PRIMARY_TARGETS := $(foreach test_dirname,$(TEST_DIRNAMES),check-swidval-primary-$(test_dirname)/swidval-passes.log)

CLEAN_SWIDTAG_TARGETS := $(foreach test_dirname,$(TEST_DIRNAMES),clean-swidtag-$(test_dirname))

all:

# The .PHONY target does not list phony clean-* targets because the top-level clean rule does not treat them as dependencies if they are phony.

.PHONY: \
  $(CHECK_SWIDTAG_TARGETS) \
  check-swidval

base.swidtag: \
  $(AUTOTOOL_SUPPORT_FILES)
	$(MAKE) clean-swidtag-base
	cd base ; ./autogen.sh
	cd base ; ./configure
	$(MAKE) -C base PYTHON=$(PYTHON) check
	$(MAKE) -C base PYTHON=$(PYTHON) installcheck
	$(MAKE) -C base PYTHON=$(PYTHON) distcheck
	$(MAKE) -C base PYTHON=$(PYTHON) $(DIST_SWIDTAG_TARGETS)
	tar \
	  -xOzf \
	  base/sample_nop-0.0.1.tar.gz \
	  sample_nop-0.0.1/swidtag/sample_nop.swidtag \
	  > _$@
	  mv _$@ $@

check: \
  $(CHECK_SWIDTAG_TARGETS)

check-swidtag-base: \
  base.swidtag \
  check-core.py
	$(PYTHON) check-core.py \
	  $<

check-swidtag-lang: \
  lang.swidtag \
  check-core.py
	$(PYTHON) check-core.py \
	  --check-lang en-gb \
	  $<

check-swidtag-configure_disable_swid_xmllint: \
  configure_disable_swid_xmllint.swidtag \
  check-core.py
	$(PYTHON) check-core.py \
	  $<
	test \
	  $$(xmllint --format $< | wc -c | tr -d ' ') \
	  -gt \
	  $$(cat $< | wc -c | tr -d ' ')

check-swidtag-tagid_file: \
  tagid_file.swidtag \
  check-core.py
	$(PYTHON) check-core.py \
	  --check-tagid_file-corpus $$(head -n1 tagid_file/var/swid/corpus-bzip2-tagId.txt) \
	  tagid_file/sample_nop-0.0.1.tar.bz2.swidtag
	$(PYTHON) check-core.py \
	  --check-tagid_file-corpus $$(head -n1 tagid_file/var/swid/corpus-lzip-tagId.txt) \
	  tagid_file/sample_nop-0.0.1.tar.lz.swidtag
	$(PYTHON) check-core.py \
	  --check-tagid_file-corpus $$(head -n1 tagid_file/var/swid/corpus-tagId.txt) \
	  tagid_file/sample_nop-0.0.1.tar.gz.swidtag
	$(PYTHON) check-core.py \
	  --check-tagid_file-corpus $$(head -n1 tagid_file/var/swid/corpus-xz-tagId.txt) \
	  tagid_file/sample_nop-0.0.1.tar.xz.swidtag
	$(PYTHON) check-core.py \
	  --check-tagid_file-corpus $$(head -n1 tagid_file/var/swid/corpus-zip-tagId.txt) \
	  tagid_file/sample_nop-0.0.1.zip.swidtag
	$(PYTHON) check-core.py \
	  --check-tagid_file-primary $$(head -n1 tagid_file/var/swid/primary-tagId.txt) \
	  $<

check-swidtag-tagname: \
  tagname.swidtag \
  check-core.py
	$(PYTHON) check-core.py \
	  --check-tagname gov.nist.sample_nop \
	  $<

check-swidtag-tagversion_file: \
  tagversion_file.swidtag \
  check-core.py
	$(PYTHON) check-core.py \
	  --check-tagversion_file 22 \
	  $<

check-swidtag-versionscheme: \
  versionscheme.swidtag \
  check-core.py
	$(PYTHON) check-core.py \
	  --check-versionscheme semver \
	  $<

check-swidval: \
  $(CHECK_SWIDVAL_CORPUS_TARGETS) \
  $(CHECK_SWIDVAL_PRIMARY_TARGETS)

check-swidval-corpus-%/swidval-passes.log: \
  %.swidtag \
  $(SWIDVAL_ZIP) \
  check-swidval.mk \
  swidval-base-requirements-satisfied.py
	rm -rf $$(dirname $@)
	mkdir -p $$(dirname $@)
	$(MAKE) \
	  PYTHON=$(PYTHON) \
	  SUBJECT_SWIDTAG=$$PWD/$$(basename $< .swidtag)/sample_nop-0.0.1.tar.gz.swidtag \
	  SWIDVAL_USECASE=corpus \
	  -C $$(dirname $@) \
	  -f $$PWD/check-swidval.mk

check-swidval-primary-%/swidval-passes.log: \
  %.swidtag \
  $(SWIDVAL_ZIP) \
  check-swidval.mk \
  swidval-base-requirements-satisfied.py
	rm -rf $$(dirname $@)
	mkdir -p $$(dirname $@)
	$(MAKE) \
	  PYTHON=$(PYTHON) \
	  SUBJECT_SWIDTAG=$$PWD/$< \
	  SWIDVAL_USECASE=primary \
	  -C $$(dirname $@) \
	  -f $$PWD/check-swidval.mk

clean: \
  $(CLEAN_SWIDTAG_TARGETS) \
  clean-swidval

clean-swidtag-%:
	x=$@ ; \
	  y=$${x#clean-swidtag-} ; \
	  rm -f _$$y.swidtag $$y.swidtag ; \
	  cd $$y ; \
	    test ! -r Makefile || make distclean || true

clean-swidval:
	find * -name 'check-swidval-*' -maxdepth 1 -type d | \
	  while read x ; do \
	    rm -rf $$x ; \
	  done

configure_disable_swid_xmllint.swidtag: \
  base.swidtag
	$(MAKE) clean-swidtag-configure_disable_swid_xmllint
	cd configure_disable_swid_xmllint ; ./autogen.sh
	cd configure_disable_swid_xmllint ; ./configure --disable-swid-xmllint
	$(MAKE) -C configure_disable_swid_xmllint PYTHON=$(PYTHON) check
	$(MAKE) -C configure_disable_swid_xmllint PYTHON=$(PYTHON) installcheck
	$(MAKE) -C configure_disable_swid_xmllint PYTHON=$(PYTHON) distcheck
	$(MAKE) -C configure_disable_swid_xmllint PYTHON=$(PYTHON) $(DIST_SWIDTAG_TARGETS)
	tar \
	  -xOzf \
	  configure_disable_swid_xmllint/sample_nop-0.0.1.tar.gz \
	  sample_nop-0.0.1/swidtag/sample_nop.swidtag \
	  > _$@
	mv _$@ $@

lang.swidtag: \
  base.swidtag
	$(MAKE) clean-swidtag-lang
	cd lang ; ./autogen.sh
	cd lang ; ./configure
	$(MAKE) -C lang PYTHON=$(PYTHON) check
	$(MAKE) -C lang PYTHON=$(PYTHON) installcheck
	$(MAKE) -C lang PYTHON=$(PYTHON) distcheck
	$(MAKE) -C lang PYTHON=$(PYTHON) $(DIST_SWIDTAG_TARGETS)
	tar \
	  -xOzf \
	  lang/sample_nop-0.0.1.tar.gz \
	  sample_nop-0.0.1/swidtag/sample_nop.swidtag \
	  > _$@
	mv _$@ $@

tagid_file/var/swid/corpus-bzip2-tagId.txt: \
  sample_tag_id.py
	$(PYTHON) sample_tag_id.py \
	  --corpus \
	  --dist-bzip2 \
	  > $@_
	mv $@_ $@

tagid_file/var/swid/corpus-lzip-tagId.txt: \
  sample_tag_id.py
	$(PYTHON) sample_tag_id.py \
	  --corpus \
	  --dist-lzip \
	  > $@_
	mv $@_ $@

# This target uses a "default" name in keeping with the convention of "make dist" implying .tar.gz.
tagid_file/var/swid/corpus-tagId.txt: \
  sample_tag_id.py
	$(PYTHON) sample_tag_id.py \
	  --corpus \
	  > $@_
	mv $@_ $@

tagid_file/var/swid/corpus-xz-tagId.txt: \
  sample_tag_id.py
	$(PYTHON) sample_tag_id.py \
	  --corpus \
	  --dist-xz \
	  > $@_
	mv $@_ $@

tagid_file/var/swid/corpus-zip-tagId.txt: \
  sample_tag_id.py
	$(PYTHON) sample_tag_id.py \
	  --corpus \
	  --dist-zip \
	  > $@_
	mv $@_ $@

tagid_file/var/swid/primary-tagId.txt: \
  sample_tag_id.py
	$(PYTHON) sample_tag_id.py \
	  --primary \
	  > $@_
	mv $@_ $@

tagid_file.swidtag: \
  base.swidtag \
  tagid_file/var/swid/corpus-bzip2-tagId.txt \
  tagid_file/var/swid/corpus-lzip-tagId.txt \
  tagid_file/var/swid/corpus-tagId.txt \
  tagid_file/var/swid/corpus-xz-tagId.txt \
  tagid_file/var/swid/corpus-zip-tagId.txt \
  tagid_file/var/swid/primary-tagId.txt
	$(MAKE) clean-swidtag-tagid_file
	cd tagid_file ; ./autogen.sh
	cd tagid_file ; ./configure
	$(MAKE) -C tagid_file PYTHON=$(PYTHON) check
	$(MAKE) -C tagid_file PYTHON=$(PYTHON) installcheck
	$(MAKE) -C tagid_file PYTHON=$(PYTHON) distcheck
	$(MAKE) -C tagid_file PYTHON=$(PYTHON) $(DIST_SWIDTAG_TARGETS)
	tar \
	  -xOzf \
	  tagid_file/sample_nop-0.0.1.tar.gz \
	  sample_nop-0.0.1/swidtag/sample_nop.swidtag \
	  > _$@
	mv _$@ $@

tagname.swidtag: \
  base.swidtag
	$(MAKE) clean-swidtag-tagname
	cd tagname ; ./autogen.sh
	cd tagname ; ./configure
	$(MAKE) -C tagname PYTHON=$(PYTHON) check
	$(MAKE) -C tagname PYTHON=$(PYTHON) installcheck
	$(MAKE) -C tagname PYTHON=$(PYTHON) distcheck
	$(MAKE) -C tagname PYTHON=$(PYTHON) $(DIST_SWIDTAG_TARGETS)
	tar \
	  -xOzf \
	  tagname/sample_nop-0.0.1.tar.gz \
	  sample_nop-0.0.1/swidtag/gov.nist.sample_nop.swidtag \
	  > _$@
	mv _$@ $@

tagversion_file.swidtag: \
  base.swidtag
	$(MAKE) clean-swidtag-tagversion_file
	cd tagversion_file ; ./autogen.sh
	cd tagversion_file ; ./configure
	$(MAKE) -C tagversion_file PYTHON=$(PYTHON) check
	$(MAKE) -C tagversion_file PYTHON=$(PYTHON) installcheck
	$(MAKE) -C tagversion_file PYTHON=$(PYTHON) distcheck
	$(MAKE) -C tagversion_file PYTHON=$(PYTHON) $(DIST_SWIDTAG_TARGETS)
	tar \
	  -xOzf \
	  tagversion_file/sample_nop-0.0.1.tar.gz \
	  sample_nop-0.0.1/swidtag/sample_nop.swidtag \
	  > _$@
	mv _$@ $@

versionscheme.swidtag: \
  base.swidtag
	$(MAKE) clean-swidtag-versionscheme
	cd versionscheme ; ./autogen.sh
	cd versionscheme ; ./configure
	$(MAKE) -C versionscheme PYTHON=$(PYTHON) check
	$(MAKE) -C versionscheme PYTHON=$(PYTHON) installcheck
	$(MAKE) -C versionscheme PYTHON=$(PYTHON) distcheck
	$(MAKE) -C versionscheme PYTHON=$(PYTHON) $(DIST_SWIDTAG_TARGETS)
	tar \
	  -xOzf \
	  versionscheme/sample_nop-0.0.1.tar.gz \
	  sample_nop-0.0.1/swidtag/sample_nop.swidtag \
	  > _$@
	mv _$@ $@
