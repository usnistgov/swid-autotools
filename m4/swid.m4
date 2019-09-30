dnl This software was developed at the National Institute of Standards
dnl and Technology by employees of the Federal Government in the course
dnl of their official duties. Pursuant to title 17 Section 105 of the
dnl United States Code this software is not subject to copyright
dnl protection and is in the public domain. NIST assumes no
dnl responsibility whatsoever for its use by other parties, and makes
dnl no guarantees, expressed or implied, about its quality,
dnl reliability, or any other characteristic.
dnl
dnl We would appreciate acknowledgement if the software is used.

dnl @synopsis SWID_SET_LANG
dnl
dnl This macro guarantees these variables are available for AC_OUTPUT:
dnl
dnl SWID_LANG
dnl
dnl @author Alex Nelson <alexander.nelson@nist.gov>
dnl @license PublicDomain

AC_DEFUN([SWID_SET_LANG],[dnl
AC_ARG_VAR([SWID_LANG],[The value of the xml:lang attribute of the root element.])dnl
m4_ifndef([SWID_LANG],[dnl
  m4_ifval([$1],dnl
    [AC_SUBST([SWID_LANG],[$1])],dnl
    [AC_SUBST([SWID_LANG],[en-us])]dnl
  )dnl
])dnl
])# SWID_SET_LANG

dnl @synopsis SWID_SET_SOFTWARECREATOR
dnl
dnl SWID_SET_SOFTWARECREATOR requires two arguments.  The first becomes
dnl the "name" attribute of the Entity element with the role
dnl "softwareCreator".  The second becomes the "regid" attribute of the
dnl same Entity element.
dnl
dnl This macro guarantees these variables are set:
dnl
dnl SWID_SOFTWARECREATOR_NAME
dnl SWID_SOFTWARECREATOR_REGID
dnl
dnl @author Alex Nelson <alexander.nelson@nist.gov>
dnl @license PublicDomain

AC_DEFUN([SWID_SET_SOFTWARECREATOR],[dnl
AC_ARG_VAR([SWID_SOFTWARECREATOR_NAME],[Name of the software creator.])dnl
AC_ARG_VAR([SWID_SOFTWARECREATOR_REGID],[Regid of the software creator.])dnl
m4_ifval([$1],dnl
  [AC_SUBST([SWID_SOFTWARECREATOR_NAME],[$1])],dnl
  [AC_MSG_ERROR([SWID_SET_SOFTWARECREATOR must be called with at least one argument.])]dnl
)dnl
m4_ifval([$2],dnl
  [AC_SUBST([SWID_SOFTWARECREATOR_REGID],[$2])],dnl
  [dnl
    m4_ifval([$PACKAGE_BUGREPORT],dnl
      [dnl
        AC_MSG_NOTICE([SWID_SOFTWARECREATOR_REGID being inferred from PACKAGE_BUGREPORT.])dnl
        AC_SUBST([SWID_SOFTWARECREATOR_REGID],[mailto:$PACKAGE_BUGREPORT])dnl
      ],dnl
      [AC_MSG_ERROR([SWID_SET_SOFTWARECREATOR needs a regid.  PACKAGE_BUGREPORT was not available to infer a mailto: URL.])]dnl
    )dnl
  ]dnl
)dnl
])# SWID_SET_SOFTWARECREATOR

dnl @synopsis SWID_SET_TAGCREATOR
dnl
dnl This macro guarantees these variables are set:
dnl
dnl SWID_TAGCREATOR_NAME
dnl SWID_TAGCREATOR_REGID
dnl
dnl If not provided as arguments 1 and 2, this macro will default to
dnl inheriting SWID_SOFTWARECREATOR_* values.
dnl
dnl @author Alex Nelson <alexander.nelson@nist.gov>
dnl @license PublicDomain

AC_DEFUN([SWID_SET_TAGCREATOR],[dnl
AC_REQUIRE([SWID_SET_SOFTWARECREATOR])dnl
AC_ARG_VAR([SWID_TAGCREATOR_NAME],[Name of the tag creator.])dnl
AC_ARG_VAR([SWID_TAGCREATOR_REGID],[Regid of the tag creator.])dnl
m4_ifndef([SWID_TAGCREATOR_NAME],[dnl
  m4_ifval([$1],dnl
    [AC_SUBST([SWID_TAGCREATOR_NAME],[$1])],dnl
    [AC_SUBST([SWID_TAGCREATOR_NAME],[$SWID_SOFTWARECREATOR_NAME])]dnl
  )dnl
])dnl
m4_ifndef([SWID_TAGCREATOR_REGID],dnl
  m4_ifval([$2],dnl
    [AC_SUBST([SWID_TAGCREATOR_REGID],[$1])],dnl
    [AC_SUBST([SWID_TAGCREATOR_REGID],[$SWID_SOFTWARECREATOR_REGID])]dnl
  )dnl
)dnl
])# SWID_SET_TAGCREATOR

dnl @synopsis SWID_SET_TAGNAME
dnl
dnl This macro guarantees this variable is available for AC_OUTPUT:
dnl
dnl SWID_TAGNAME
dnl
dnl @author Alex Nelson <alexander.nelson@nist.gov>
dnl @license PublicDomain

AC_DEFUN([SWID_SET_TAGNAME],[dnl
AC_ARG_VAR([SWID_TAGNAME],[The name of the tag, to be stored as an attribute of the root element.])dnl
m4_ifndef([SWID_TAGNAME],[dnl
  m4_ifval([$1],dnl
    [AC_SUBST([SWID_TAGNAME],[$1])],dnl
    [AC_SUBST([SWID_TAGNAME],[$PACKAGE_NAME])]dnl
  )dnl
])dnl
])# SWID_SET_TAGNAME

dnl @synopsis SWID_SET_VERSION_SCHEME
dnl
dnl This macro guarantees this variable is available for AC_OUTPUT:
dnl
dnl SWID_VERSION_SCHEME
dnl
dnl @author Alex Nelson <alexander.nelson@nist.gov>
dnl @license PublicDomain

AC_DEFUN([SWID_SET_VERSION_SCHEME],[dnl
AC_ARG_VAR([SWID_VERSION_SCHEME],[The versionScheme attribute of the root element.])dnl
m4_ifndef([SWID_VERSION_SCHEME],[dnl
  m4_ifval([$1],dnl
    [AC_SUBST([SWID_VERSION_SCHEME],[$1])],dnl
    [AC_SUBST([SWID_VERSION_SCHEME],[unknown])]dnl
  )dnl
])dnl
])# SWID_SET_VERSION_SCHEME

dnl @synopsis SWID_SUBST
dnl
dnl This macro guarantees these variables are available for AC_OUTPUT:
dnl
dnl SWID_LANG
dnl SWID_TAGNAME
dnl SWID_VERSION_SCHEME
dnl SWID_XMLLINT
dnl
dnl AM_PATH_PYTHON is also guaranteed to run at least once,
dnl via AC_REQUIRE.
dnl
dnl @author Alex Nelson <alexander.nelson@nist.gov>
dnl @license PublicDomain

AC_DEFUN([SWID_SUBST],[dnl
AC_REQUIRE([SWID_SET_TAGCREATOR])dnl
AC_REQUIRE([SWID_SET_LANG])dnl
AC_REQUIRE([SWID_SET_TAGNAME])dnl
AC_REQUIRE([SWID_SET_VERSION_SCHEME])dnl
AC_ARG_VAR([SWID_XMLLINT],[An alias used for detecting 'xmllint', to prevent clobbering other variables that may depend on different path spelling for the discovered xmllint.])dnl
AC_ARG_ENABLE([swid-xmllint],dnl
    AS_HELP_STRING([--disable-swid-xmllint], [Disable use of xmllint for SWID tag formatting]),dnl
    [],dnl
    [enable_swid_xmllint=yes])dnl
AS_IF([test "x$enable_swid_xmllint" != "xno"],[dnl
  AC_CHECK_PROG([SWID_XMLLINT],[xmllint],[xmllint],[no])dnl
  AM_CONDITIONAL([SWID_USE_XMLLINT],dnl
      [test "x$SWID_XMLLINT" == "xxmllint" ])dnl
  AC_SUBST([SWID_XMLLINT])dnl
],[dnl
  AM_CONDITIONAL([SWID_USE_XMLLINT],[false])dnl
  AC_SUBST([SWID_XMLLINT],[false])dnl
])dnl
AC_REQUIRE([AM_PATH_PYTHON])
])# SWID_SUBST
