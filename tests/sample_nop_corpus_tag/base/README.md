# Sample application: Nop

This directory contains a source tree for a simple application that attempts to do nothing well.


## Test purpose

To demonstrate the minimal changes to an Autotools-based source tree to generate a SWID Corpus tag.


### Source code differences from original application

To alleviate the distributor from needing to make complex macro calls, supporting files are available for soft-linking into the source tree.  Three files are soft-linked from the top directory of the SWID Autotools repository:

* `/include/swid.am`
* `/lib/swidtag.py`
* `/m4/swid.m4`

This was done so this Git repository could be tracked as a Git submodule, as demonstrated in the [incorporation](../../incorporation) unit tests.

To ensure these files are included in the output of `make dist`, the `EXTRA_DIST` Automake variable includes the linked file (see `include/Makefile.am` and `lib/Makefile.am`)

The top `Makefile.am` adds Automake-level SWID hooks by running an `include` directive:

```
diff -r ../../sample_nop/Makefile.am Makefile.am
12a13,16
> 
> DIST_SUBDIRS = include lib src
> 
> include $(top_srcdir)/include/swid.am
```

Last, `configure.ac` minimally requires two macros distinct to SWID be called: `SWID_SET_SOFTWARECREATOR` and `SWID_SUBST`.  The remainder of the changes to `configure.ac` are otherwise fairly boilerplate:

```
diff -r ../sample_nop/configure.ac base/configure.ac
19a20,24
> AC_CONFIG_MACRO_DIR([m4])
> 
> # Populate SWID information.
> SWID_SET_SOFTWARECREATOR(["National Institute of Standards and Technology"], [nist.gov])
> SWID_SUBST
32a38,39
>                  include/Makefile
>                  lib/Makefile
```


### Behavioral differences from original application

A SWID Primary tag is created in the distribution tarball.

A SWID Corpus tag is created alongside the distribution tarball.

The above is also true for zips and other `make dist` target formats.
