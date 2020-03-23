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

all: \
  swidval-0.5.0-swidval.zip

swidval-0.5.0-swidval.zip: \
  swidval-0.5.0-swidval.zip.sha512
	wget -O _$@ https://csrc.nist.gov/CSRC/media/Projects/Software-Identification-SWID/tools/$@
	test "x$$(openssl dgst -sha512 _$@ | awk '{print($$NF)}')" == "x$$(head -n1 $< | awk '{print($$NF)}')" \
	  || (echo "ERROR:Makefile:$@ SHA-512 failed to verify." >&2 ; exit 1)
	touch _$@
	mv _$@ $@
