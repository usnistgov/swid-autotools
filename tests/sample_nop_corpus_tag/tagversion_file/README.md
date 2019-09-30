# Sample application: Nop

This directory contains a source tree for a simple application that attempts to do nothing well.


## Test purpose

To modify the tagversion of the SWID tag (i.e. the version of the tag itself, instead of the application).


### Source code differences from original application with SWID

To handle the case where a SWID tag needs to record a version other than `1`, the `swid.am` Automake hook checks for a file in a hard-coded path: `$(top_srcdir)/var/swid/corpus-tagVersion.txt`.  If that file exists, its contents are assumed (though tested) to be an integer, to be recorded in the tag's root attribute `@tagVersion`.

Though the file is named `corpus-tagVersion.txt`, note that it also affects the version of the primary tag included within the distribution archive.  This is because the embedded primary tag and the corpus tag would be generated at the same time.

If the `tagVersion` file is to be supplied, it should be included by the `AC_CONFIG_FILES` macro calling down the Automake file chain, down to `$(top_srcdir)/var/swid/Makefile.am` that includes an `EXTRA_DIST` definition.

```
diff -r ../base/Makefile.am Makefile.am
14c14
< DIST_SUBDIRS = include lib src
---
> DIST_SUBDIRS = include lib var/swid src
diff -r ../base/configure.ac configure.ac
40c40,41
<                  src/Makefile])
---                                                                                      
>                  src/Makefile
>                  var/swid/Makefile])
```


## Design rationale

Usage of a hard-coded file path is a design decision.  A build system would need to have some mechanism to refer to the history of previously built SWID tags for a fixed version of an application.  Tracking the build in a file in the source tree was seen as one way to record the information which potentially induced the least software dependencies.  As with other features of this code base, this mechanism is open to feedback.


### Behavioral differences from original application with SWID

The root element's `tagVersion` attribute records `22` (the contents of `$(top_srcdir)/var/swid/corpus-tagVersion.txt`).
