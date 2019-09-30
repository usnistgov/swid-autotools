# Corpus tag unit tests

This directory tests GNU Autotool macros that generate Corpus tags.  The [`base/`](base/) directory contains the minimal modifications to the [sample C application](../sample_not/), and its [README](base/README.md) documents the necessary changes.  Each other directory here documents changes in addition to the "base"-level changes.


## Features tested

* [`configure_disable_swid_xmllint`](configure_disable_swid_xmllint) - By default, `xmllint` is run to confirm well-formedness of the SWID tag, as well as pretty-print it.  This test shows `xmllint` can be disabled in the build process, potentially removing a build dependency.
* [`lang`](lang) - Changing the top-level language in the SWID tag.
* [`tagname`](tagname) - Changing the basename of the SWID tag.
* [`tagversion_file`](tagversion_file) - Changing the `tagVersion` of the SWID tag.
* [`versionscheme`](versionscheme) - Changing the `versionScheme` of the SWID tag.


## Running SWIDVal

The Make target `check` generates SWID tags.  The target `check-swidval` runs [SWIDVal](https://csrc.nist.gov/Projects/Software-Identification-SWID/resources) to validate the generated tag files.  However, at the time of this writing, automated retrieval of SWIDVal only functions semi-consistently because of a certificate verification issue not present in web browsers, but present in some command-line utilities.

As a workaround, a user interested in running the SWIDVal unit tests can do the following:

1. Manually download SWIDVal, the zip file, from the above link.
2. Move the SWIDVal zip file to this directory.
3. Run `touch swidval-0.5.0-swidval.zip` to update its timestamp.

Then the interested user can run `make check-swidval`.
