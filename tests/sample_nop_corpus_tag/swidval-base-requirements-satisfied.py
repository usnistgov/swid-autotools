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
This program takes as input the validation-result.xml file generated by swidval, and prints to stderr the number of base requirements that failed.  On counting no assessment results of any kind, or on counting more than 0 FAIL statuses, the program exits non-0.
"""

__version__ = "0.1.1"

import os
import logging
import sys
import xml.etree.ElementTree as ET

_logger = logging.getLogger(os.path.basename(__file__))

def main():
    nsmap = {"d": "http://csrc.nist.gov/ns/decima/results/1.0"}
    root_tree = ET.parse(args.in_xml)
    root_elem = root_tree.getroot()
    assessment_result_count = 0
    fail_count = 0
    for elem in root_elem.findall("d:results//d:base-requirement/d:status", nsmap):
        assessment_result_count += 1
        if elem.text == "FAIL":
            fail_count += 1
    _logger.debug("assessment_result_count=%d" % assessment_result_count)
    _logger.debug("fail_count=%d" % fail_count)
    if assessment_result_count < 2:
        _logger.error("Failed to retrieve assessment results.")
        rc = 1
    elif fail_count > 0:
        _logger.error("Some assessments failed.")
        rc = 1
    else:
        rc = 0
    sys.exit(rc)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug", action="store_true")
    parser.add_argument("in_xml")
    args = parser.parse_args()
    logging.basicConfig(level=logging.DEBUG if args.debug else logging.INFO)
    main()
