# Sample application: Nop

This directory contains a source tree for a simple application that attempts to do nothing well.


## Test purpose

To modify the name of the SWID tag file, using the `SWID_SET_TAGNAME` macro.


### Source code differences from original application with SWID

Before calling `SWID_SUBST`, the macro `SWID_SET_TAGNAME` is called to set the tag name to a non-default.

```
diff ../base/configure.ac configure.ac
23a24
> SWID_SET_TAGNAME([gov.nist.sample_nop])
```


### Behavioral differences from original application with SWID

The in-tarball file that would have been called `/swidtag/sample_nop.swidtag` is instead called `/swidtag/gov.nist.sample_nop.swidtag`.
