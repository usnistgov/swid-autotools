# Sample application: Nop

This directory contains a source tree for a simple application that attempts to do nothing well.


## Test purpose

To modify the version scheme recorded in the SWID tag, using the `SWID_SET_VERSION_SCHEME` macro.


### Source code differences from original application with SWID

Before calling `SWID_SUBST`, the macro `SWID_SET_VERSION_SCHEME` is called to set the version scheme to Semantic Versioning.

```
diff ../base/configure.ac configure.ac
23a24
> SWID_SET_VERSION_SCHEME([semver])
```


### Behavioral differences from original application with SWID

The root element's `versionScheme` attribute records `semver`.
