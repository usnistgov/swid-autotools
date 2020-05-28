#                                               -*- Autoconf -*-
# Process this file with autoconf to produce a configure script.

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

AC_PREREQ([2.69])
AC_INIT([sample_nop], [0.0.1])
AM_INIT_AUTOMAKE
AC_CONFIG_SRCDIR([src/nop.c])
AC_CONFIG_HEADERS([config.h])
AC_CONFIG_MACRO_DIR([m4])

# Populate SWID information.
SWID_SET_SOFTWARECREATOR(["National Institute of Standards and Technology"], [nist.gov])
SWID_SUBST

# Checks for programs.
AC_PROG_CC

# Checks for libraries.

# Checks for header files.

# Checks for typedefs, structures, and compiler characteristics.

# Checks for library functions.

AC_CONFIG_FILES([Makefile
                 include/Makefile
                 lib/Makefile
                 src/Makefile
                 var/swid/Makefile])
AC_OUTPUT
