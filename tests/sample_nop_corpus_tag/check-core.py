#!/usr/bin/env python

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

"""
This file contains toggle-able tests for SWID tags generated in this directory's unit tests.
"""

__version__ = "0.1.0"

import os
import logging
import xml.etree.ElementTree as ET

_logger = logging.getLogger(os.path.basename(__file__))

def main():
    root = ET.parse(args.in_swidtag)
    root_elem = root.find(".")

    try:
        assert args.check_lang == root_elem.attrib["{http://www.w3.org/XML/1998/namespace}lang"]
    except:
        _logger.info("args.check_lang=%r" % args.check_lang)
        #_logger.info("root_elem.attrib=%r" % root_elem.attrib)
        _logger.info("root_elem.attrib[\"xml:lang\"]=%r" % root_elem.attrib["{http://www.w3.org/XML/1998/namespace}lang"])
        raise

    if args.check_tagid_file_corpus:
        try:
            assert args.check_tagid_file_corpus == root_elem.attrib["tagId"]
        except:
            _logger.info("args.check_tagid_file_corpus=%r" % args.check_tagid_file_corpus)
            _logger.info("root_elem.attrib[\"tagId\"]=%r" % root_elem.attrib["tagId"])
            raise

    if args.check_tagid_file_primary:
        try:
            assert args.check_tagid_file_primary == root_elem.attrib["tagId"]
        except:
            _logger.info("args.check_tagid_file_primary=%r" % args.check_tagid_file_primary)
            _logger.info("root_elem.attrib[\"tagId\"]=%r" % root_elem.attrib["tagId"])
            raise

    try:
        assert args.check_tagname == root_elem.attrib["name"]
    except:
        _logger.info("args.check_tagname=%r" % args.check_tagname)
        _logger.info("root_elem.attrib[\"name\"]=%r" % root_elem.attrib["name"])
        raise

    try:
        assert args.check_tagversion_file == root_elem.attrib["tagVersion"]
    except:
        _logger.info("args.check_tagversion_file=%r" % args.check_tagversion_file)
        _logger.info("root_elem.attrib[\"tagVersion\"]=%r" % root_elem.attrib["tagVersion"])
        raise

    try:
        assert args.check_versionscheme == root_elem.attrib["versionScheme"]
    except:
        _logger.info("args.check_versioncheme=%r" % args.check_versionscheme)
        _logger.info("root_elem.attrib[\"versionScheme\"]=%r" % root_elem.attrib["versionScheme"])
        raise

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-lang", default="en-us")
    parser.add_argument("--check-tagname", default="sample_nop")
    parser.add_argument("--check-tagid_file-corpus") #(Default is random, hence not checked.)
    parser.add_argument("--check-tagid_file-primary") #(Default is random, hence not checked.)
    parser.add_argument("--check-tagversion_file", default="1")
    parser.add_argument("--check-versionscheme", default="unknown")
    parser.add_argument("in_swidtag")
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO)
    main()
