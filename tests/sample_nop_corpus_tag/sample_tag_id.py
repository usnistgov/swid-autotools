#!/usr/bin/env python3

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
This script creates an example constant UUID.
"""

import uuid

def main():
    if args.corpus:
        if args.dist_bzip2:
            dist = "bzip2"
        elif args.dist_gzip:
            dist = "gzip"
        elif args.dist_lzip:
            dist = "lzip"
        elif args.dist_xz:
            dist = "xz"
        elif args.dist_zip:
            dist = "zip"
        else:
            dist = "gzip"
        print(str(uuid.uuid5(uuid.NAMESPACE_URL, "http://example.org/demonstration%20swidtag%20uuid%20/corpus" + dist)))
    elif args.primary:
        print(str(uuid.uuid5(uuid.NAMESPACE_URL, "http://example.org/demonstration%20swidtag%20uuid%20/primary")))

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--corpus", action="store_true")
    parser.add_argument("--primary", action="store_true")
    dist_group = parser.add_mutually_exclusive_group()
    dist_group.add_argument("--dist-bzip2", action="store_true")
    dist_group.add_argument("--dist-gzip", action="store_true")
    dist_group.add_argument("--dist-lzip", action="store_true")
    dist_group.add_argument("--dist-xz", action="store_true")
    dist_group.add_argument("--dist-zip", action="store_true")
    args = parser.parse_args()
    main()
