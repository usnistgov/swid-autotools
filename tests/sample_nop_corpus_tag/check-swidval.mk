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

SWIDVAL_USECASE ?= corpus

SWIDVAL_ZIP ?= ../swidval-0.5.0-swidval.zip

SUBJECT_SWIDTAG ?=
ifeq ($(SUBJECT_SWIDTAG),)
$(error SUBJECT_SWIDTAG not provided)
endif

all: \
  swidval-passes.log

swidval-0.5.0.jar: \
  $(SWIDVAL_ZIP)
	unzip $<

swidval-passes.log: \
  ../swidval-base-requirements-satisfied.py \
  validation-result.xml
	$(PYTHON) ../swidval-base-requirements-satisfied.py \
	  --debug \
	  validation-result.xml
	touch $@

validation-result.xml: \
  $(SUBJECT_SWIDTAG) \
  swidval-0.5.0.jar
	java -jar swidval-0.5.0.jar \
	  -usecase $(SWIDVAL_USECASE) \
	  $(SUBJECT_SWIDTAG)
