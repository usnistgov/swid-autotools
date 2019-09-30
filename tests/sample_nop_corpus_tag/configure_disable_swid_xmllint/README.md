# Sample application: Nop

This directory contains a source tree for a simple application that attempts to do nothing well.


## Test purpose

To confirm that `xmllint` (and this `libxml2`) is not a hard requirement to use these Autotool macros to generate SWID tags.


### Source code differences from original application with SWID

No source is modified for this test.  Instead, the call to `./configure` has the additional flag `--disable-swid-xmllint`.


### Behavioral differences from original application with SWID

The generated SWID tags are not run through `xmllint` (confirmable by a lack of indentation).
