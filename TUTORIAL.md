# SWID Autotools Incorporation Tutorial

The SWID Autotools project adds SWID features to projects based on the GNU Autotools build chain.  This document illustrates the entire procedure for incorporating SWID corpus tag support into Autotools.

The feature additions are made via modifications to `configure.ac` and `Makefile.am`, and adding some library files to a project's source tree.


## Demonstration with a sample Autotools project

If you don't have a project ready to modify, this project includes a simple program as an example.  The heart of the program is a basic implementation of the `true` command, always exiting 0 when called and not doing any operations otherwise.  Source: [`nop.c`](tests/sample_nop/src/nop.c).

```
int main(int argc, char** argv) {
  return 0;
}
```

The [source tree](tests/sample_nop) for the `sample_nop` project includes the bare minimum to have a "configure-make-make-install" process function, starting from an `autogen.sh` call.  That source tree was also written to ensure a stricter `make check` test suite, [`make distcheck`](https://www.gnu.org/software/automake/manual/html_node/Checking-the-Distribution.html), passes.  `make distcheck` confirms the test suite passes whether run from the source tree or from a built and shipped archive.

An alternative sample program is available in a [Hello World](https://www.gnu.org/software/automake/manual/automake.html#Hello-World) from the Automake documentation.  `autoscan` created the `configure.ac` in this project's `sample_nop`.


### Tracking SWID support

Macros in m4 have a long history of being copied around as code segments.  This project is structured so a developer who wishes to do more specific version tracking can import files using `git submodule` and soft-linking.  If submodules and soft-linking are not desired, files (or even functions) can still be copied into developers' source tree.

In the project's source tree, some additional files need to be incorporated from this project.  `make explain` illustrates the end goal; this tutorial will show two ways to reach that goal.

```
These are the changes to configure.ac and Makefile.am needed to add SWID tags (noting that the NIST reference should be replaced with the implementing organization's authorship information):

diff tests/sample_nop/configure.ac tests/sample_nop_corpus_tag/base/configure.ac || true
19a20,24
> AC_CONFIG_MACRO_DIR([m4])
> 
> # Populate SWID information.
> SWID_SET_SOFTWARECREATOR(["National Institute of Standards and Technology"], [nist.gov])
> SWID_SUBST
32a38,39
>                  include/Makefile
>                  lib/Makefile
diff tests/sample_nop/Makefile.am tests/sample_nop_corpus_tag/base/Makefile.am || true
21a22,25
> 
> DIST_SUBDIRS = include lib src
> 
> include $(top_srcdir)/include/swid.am

Note the lib/ and include/ directories also have support files soft-linked in and referenced by their Makefile.am files.

include/swid.am
lib/swidtag.py
m4/swid.m4

Those files can be copied into the source tree if soft-links and Git submodule tracking are not desired.

Last, note that the soft-linked files are added to EXTRA_DIST.

grep EXTRA_DIST tests/sample_nop_corpus_tag/base/{include,lib}/Makefile.am
tests/sample_nop_corpus_tag/base/include/Makefile.am:EXTRA_DIST = swid.am
tests/sample_nop_corpus_tag/base/lib/Makefile.am:EXTRA_DIST = swidtag.py
```

In summary, these are the files that need to be incorporated into the project's source tree, in the same directories as they are in in the SWID Autotools project:

```
include/swid.am
lib/swidtag.py
m4/swid.m4
```

And these are the files that will require patching (illustrated with the diff in `make explain`) to link the incorporated files into the build system:

```
Makefile.am
configure.ac
include/Makefile.am
lib/Makefile.am
```

The two methods start the same way, from a fresh copy of the project's source tree.


#### Adding SWID support with file copying

This method is simply copying the above files into the project tree, from the root of this directory.

Running `make check-copying` in the directory `tests/incorporation` will demonstrate this.  Note that the patching is done with rsync from another unit test directory, but in other code bases the patching should be done by hand.


#### Adding SWID support with a Git submodule

This method incorporates the library files with `git submodule` and soft-linking.

Starting from the root of the project's source tree, ensure it is maintaining a Git repository for itself.  If it isn't, initialize a Git repository:

```
git init .
```

Next, track the SWID Autotools repository as a Git submodule, committing that change:

```
git submodule add https://github.com/usnistgov/swid-autotools deps/swid-autotools
git commit .gitmodules deps/swid-autotools
```

(The top-level `deps/` directory is but one practice for tracking other code bases submodules.  Any directory or location will do, but paths referenced below would need to be updated.)

Then, soft-link the library files into their appropriate locations.  The soft links can be tracked with `git add`.

```
ln -s deps/swid-autotools/include/swid.am include/swid.am
git add include/swid.am
ln -s deps/swid-autotools/lib/swidtag.py lib/swidtag.py
git add lib/swidtag.py
ln -s deps/swid-autotools/m4/swid.m4 m4/swid.m4
git add m4/swid.m4
```

A `git commit` at this point will add the links to the source tree.

Later, when the source repository is cloned in another location, the submodule will need to be initialized (requiring networking with the `update` command), else the build system will report errors because of broken links:

```
git submodule init
git submodule update
```


#### Tests of SWID support methods

Both the Git submodule mechanism and the file-copying mechanism are run as a unit test, `make check-incorporation`.  This is a separate test because the Git submodule test requires networking.


## Further configuration

The [corpus tag test directory](tests/sample_nop_corpus_tag) tests features of the SWID Autotool macros, including `./configure` flags, versioning SWID tags themselves (separately from the software versioning), and other features.  That directory and its subdirectories demonstrate the features.
