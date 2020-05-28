# Sample application: Nop

This directory contains a source tree for a simple application that attempts to do nothing well.


## Test purpose

To modify the tagId of the SWID tag (i.e. the identifier of the tag itself).


### Source code differences from original application with SWID

To handle the case where a SWID tag needs to have a specified identifier, such as when planning tag construction in a build chain, or when updating a prior version of a tag, the `swid.am` Automake hook checks for a file in a hard-coded path: `$(top_srcdir)/var/swid/corpus-tagId.txt`.  If that file exists, its contents are assumed to be one line specifying a string suitable as a tagId, to be recorded in the tag's root attribute `@tagId`.

Files of similar purpose are employed for some variant tags.  The file `primary-tagId.txt` contains the tag identifier for the primary tag included within the distribution archive.  For other `dist` targets, other corpus tag files are detected alongside `corpus-tagId.txt`:
* corpus-bzip2-tagId.txt
* corpus-lzip-tagId.txt
* corpus-xz-tagId.txt
* corpus-zip.txt
These mirror the similarly-named `dist` targets.  Keeping with the convention of `dist-gzip` being the default `dist` target, `corpus-tagId.txt` behaves as the default corpus tag ID holder.

If the `tagId` file is to be supplied, it should be included by the `AC_CONFIG_FILES` macro calling down the Automake file chain, down to `$(top_srcdir)/var/swid/Makefile.am` that includes an `EXTRA_DIST` definition.

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

The embedded primary tag root element's `tagId` attribute records `20d21d5c-ccdf-5e46-bc4a-6504e8c813b8` (the contents of `$(top_srcdir)/var/swid/primary-tagId.txt`).

The corpus tag root element's `tagId` attribute records the value of the corresponding "dist" file:
* `b9ca597a-ddaa-598c-8510-d75ac2ea04df` - `corpus-bzip2-tagId.txt`
* `dbe701d3-2cd8-575e-84b5-10c5947e13da` - `corpus-lzip-tagId.txt`
* `12b53abb-e0d7-5360-8df4-4092ef81edc7` - `corpus-tagId.txt`
* `adc14661-5219-5bf7-9fa0-de6e9af38540` - `corpus-xz-tagId.txt`
* `0f306175-c8c2-5549-97ab-38981db13ab9` - `corpus-zip-tagId.txt`
