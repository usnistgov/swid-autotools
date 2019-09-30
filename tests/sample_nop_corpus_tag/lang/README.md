# Sample application: Nop

This directory contains a source tree for a simple application that attempts to do nothing well.


## Test purpose

To modify the language recorded in the SWID tag, using the `SWID_SET_LANG` macro.


### Source code differences from original application with SWID

Before calling `SWID_SUBST`, the macro `SWID_SET_LANG` is called to set the language to the British English variant.

```
diff ../base/configure.ac configure.ac
23a24
> SWID_SET_LANG([en-gb])
```


### Behavioral differences from original application with SWID

The root element's `xml:lang` attribute records `en-gb`.
