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
This script creates an unsigned SWID tag for a distribution bundle or directory.  The contents of a distribution directory can be described as a Primary SWID tag, if using this script as part of a dist-hook Automake rule.  The contents of an individual file, such as an archive file (.tar.gz, .zip, self-unpacking .exe, etc.), can also be represented as an annotated SWID tag.

This script takes as input the path to the distribution directory or file, and several parameters for authoring metadata.  The path to the output file is also required, in order to determine relative pathing of files.

Some XML ElementTree logistics in this script used this code as reference:

    https://github.com/strongswan/swidGenerator/blob/master/swid_generator/generators/swid_generator.py
"""

__version__ = "0.7.1"

import os
import sys
import hashlib
import collections
import re
import xml.etree.ElementTree as ET
import logging
import uuid

_logger = logging.getLogger(os.path.basename(__file__))

rx_python_version_definition = re.compile(r"""^__version__(\s*)=(\s*)(?P<openquote>['"])(?P<version_value>.+)(?P=openquote).*$""")

def relative_path_to_directory(source_path, dest_directory):
    """
    This returns the path comprised of ".." ascensions that would be needed to get from the source_path to the destination directory.
    In the context of this code base, this is most likely to return "." or ".." for most of its use cases.
    """
    normed_source_path = os.path.realpath(source_path)
    normed_dest_directory = os.path.realpath(dest_directory)

    source_path_dirname = os.path.dirname(normed_source_path)
    if source_path_dirname == normed_dest_directory:
        return "."
    elif os.path.dirname(source_path_dirname) == normed_dest_directory:
        return ".."

    # Future use cases can be supported with os.path.commonprefix and looping until a match is found, but that may require directory paths fed into this function represent actual directories.  One possible use case of this function would generate element trees from text lists.  When that use case becomes supported this function will require further development and testing.
    _logger.info("source_path = %r." % source_path)
    _logger.info("dest_directory = %r." % dest_directory)
    raise NotImplementedError("TODO")

def file_path_to_file_element(child_path):
    # Annotate files.
    child_name = os.path.basename(child_path)
    file_element = ET.Element("File")
    file_element_stat = os.stat(child_path)
    file_element.set("size", str(file_element_stat.st_size))
    sha256obj = hashlib.sha256()
    sha512obj = hashlib.sha512()
    with open(child_path, "rb") as child_fh:
        buf = child_fh.read(2**20)
        sha256obj.update(buf)
        sha512obj.update(buf)
    file_element.set("SHA256:hash", sha256obj.hexdigest().lower())
    file_element.set("SHA512:hash", sha512obj.hexdigest().lower())

    # Try adding version information for Python files.
    if child_name.endswith(".py"):
        # Use crude scan for __version__ instead of calling arbitrary scripts by opening a Python subprocess.
        with open(child_path, "r") as child_fh:
            for line in child_fh:
                cleaned_line = line.strip()
                maybe_match = rx_python_version_definition.search(cleaned_line)
                if maybe_match:
                    file_element.set("version", maybe_match.group("version_value"))
                    break
    file_element.set("name", child_name)
    return file_element

def directory_path_to_directory_element(directory_path):
    # Convert distribution directory walk to Payload element.
    # Cache directory Element references by relative path.
    #   Key: Path relative to root of walk.
    #   Value: ET.Element.
    rel_dirpath_element = dict()

    # Prime with root directory.
    rel_dirpath_element[""] = ET.Element("Directory")
    rel_dirpath_element[""].set("name", os.path.basename(directory_path))

    directory_path_strlen = len(directory_path) + 1
    def _on_walk_error(e):
        """Since this should never happen, fail loudly."""
        raise(e)

    for (dirpath, dirnames, filenames) in os.walk(directory_path, onerror=_on_walk_error):
        # rel_dirpath: Relative path, no leading (c/o +1 above) or trailing slashes.
        rel_dirpath = dirpath[ directory_path_strlen : ].rstrip("/")
        # Ignore one self-referential directory: top-level swidtag/.
        if rel_dirpath == "":
            dirnames = [ x for x in dirnames if x != "swidtag" ]
        elif rel_dirpath == "swidtag" or rel_dirpath.startswith("swidtag/"):
            continue

        e = rel_dirpath_element[rel_dirpath]

        # Guarantee remainder of walk will visit in sorted directory order.
        dirnames.sort()

        for childname in sorted(dirnames + filenames):
            childpath = os.path.join(dirpath, childname)
            rel_childpath = os.path.join(rel_dirpath, childname)
            if childname in dirnames:
                # Cache directory references.
                ce = ET.Element("Directory")
                rel_dirpath_element[rel_childpath] = ce
                ce.set("name", childname)
            else:
                ce = file_path_to_file_element(childpath)
            e.append(ce)
    return rel_dirpath_element[""]

def main():
    # Build Payload element by walking distribution directory.
    swidtag = ET.Element("SoftwareIdentity")

    swidtag.set("xmlns", "http://standards.iso.org/iso/19770/-2/2015/schema.xsd")
    swidtag.set("xmlns:SHA256", "http://www.w3.org/2001/04/xmlenc#sha256")
    swidtag.set("xmlns:SHA512", "http://www.w3.org/2001/04/xmlenc#sha512")
    swidtag.set("xmlns:n8060", "http://csrc.nist.gov/ns/swid/2015-extensions/1.0")

    if args.corpus:
        swidtag.set("corpus", "true")

    if args.lang == "":
        raise ValueError("--lang parameter cannot be blank.")
    swidtag.set("xml:lang", args.lang)

    if args.name == "":
        raise ValueError("--name parameter cannot be blank.")
    swidtag.set("name", args.name)

    tag_id = str(uuid.uuid4())
    swidtag.set("tagId", tag_id)

    tag_version = None
    if not args.tag_version is None:
        tag_version = str(args.tag_version)
    elif not args.tag_version_file is None:
        with open(args.tag_version_file, "r") as tag_version_fh:
            tag_version_str = tag_version_fh.read(8).strip()
            tag_version_int = int(tag_version_str)
            tag_version = str(tag_version_int)
    if tag_version is None:
        # Assign default.
        tag_version = "1"
    swidtag.set("tagVersion", tag_version)

    if args.version == "":
        raise ValueError("--version parameter cannot be blank.")
    swidtag.set("version", args.version)

    if args.version_scheme == "":
        raise ValueError("--version-scheme parameter cannot be blank.")
    swidtag.set("versionScheme", args.version_scheme)

    # Set up entities, possibly consolidating.
    #   Key: (name, regid)
    #   Value: Set
    entity_role_sets = collections.defaultdict(set)

    if args.aggregator_name or args.aggregator_regid:
        if args.aggregator_name and args.aggregator_regid:
            entity_role_sets[(args.aggregator_name, args.aggregator_regid)].add("aggregator")
        else:
            raise ValueError("If supplying an aggregator, the name and regid must both be supplied.")

    if args.softwarecreator_name == "":
        raise ValueError("--softwarecreator-name parameter cannot be blank.")
    if args.softwarecreator_regid == "":
        raise ValueError("--softwarecreator-regid parameter cannot be blank.")
    entity_role_sets[(args.softwarecreator_name, args.softwarecreator_regid)].add("softwareCreator")

    if args.tagcreator_name == "":
        raise ValueError("--tagcreator-name parameter cannot be blank.")
    if args.tagcreator_regid == "":
        raise ValueError("--tagcreator-regid parameter cannot be blank.")
    entity_role_sets[(args.tagcreator_name, args.tagcreator_regid)].add("tagCreator")

    for (name, regid) in sorted(entity_role_sets.keys()):
        e = ET.Element("Entity")
        e.set("name", name)
        e.set("regid", regid)
        e.set("role", " ".join(sorted(entity_role_sets[(name, regid)])))
        swidtag.append(e)

    if args.link_describedby:
        e = ET.Element("Link")
        e.set("href", args.link_describedby)
        e.set("rel", "describedby")
        swidtag.append(e)

    if args.evidence:
        footprint_element = ET.Element("Evidence")
    elif args.payload:
        footprint_element = ET.Element("Payload")
    else:
        raise NotImplementedError("File system footprint container element not implemented.  (Expecting --evidence or --payload.)")
    footprint_element.set("n8060:pathSeparator", os.path.sep)
    footprint_element.set("n8060:envVarPrefix", "$")
    footprint_element.set("n8060:envVarSuffix", "")
    swidtag.append(footprint_element)

    distribution_paths = set([x for x in args.distribution_path])
    for distribution_path in sorted(distribution_paths):

        if os.path.isdir(distribution_path):
            element_from_path = directory_path_to_directory_element(distribution_path)
            # Overwrite the root directory's name with the relative path from the swidtag.
            element_from_path.set(
              "name",
              relative_path_to_directory(args.out_swidtag, distribution_path)
            )
            footprint_element.append(element_from_path)
        elif os.path.isfile(distribution_path):
            # Induce containing directory.
            element_containing_path = ET.Element("Directory")
            element_containing_path.set(
              "name",
              relative_path_to_directory(
                args.out_swidtag,
                os.path.dirname(distribution_path)
              )
            )
            footprint_element.append(element_containing_path)
            element_from_path = file_path_to_file_element(distribution_path)
            element_containing_path.append(element_from_path)
        else:
            raise NotImplementedError("Distribution path is neither a file nor a directory: %r." % distribution_path)

    with open(args.out_swidtag, "w") as out_fh:
        out_encoding = "UTF-8" if sys.version_info[0] < 3 else "unicode"
        out_fh.write(ET.tostring(swidtag, encoding=out_encoding))

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug", action="store_true")
    parser.add_argument("--corpus", action="store_true")
    parser.add_argument("--lang", required=True)
    parser.add_argument("--link-describedby", help="URL for documentation of this swidtag.")
    parser.add_argument("--name", required=True)
    parser.add_argument("--aggregator-name")
    parser.add_argument("--aggregator-regid")
    parser.add_argument("--softwarecreator-name", required=True)
    parser.add_argument("--softwarecreator-regid", required=True)
    parser.add_argument("--tagcreator-name", required=True)
    parser.add_argument("--tagcreator-regid", required=True)
    parser.add_argument("--version", required=True)
    parser.add_argument("--version-scheme", required=True)

    walk_source_group = parser.add_mutually_exclusive_group(required=True)
    walk_source_group.add_argument("--distribution-path", action="append", help="Path to existing file or directory to incorporate into the SWID tag.  Can be given multiple times.  Files will have a containing directory element induced to track relative pathing.")
    #TODO Left for future implementation.
    #walk_source_group.add_argument("--file-manifest")

    tree_group = parser.add_mutually_exclusive_group(required=True)
    tree_group.add_argument("--evidence", action="store_true", help="The element to use for an evidence tag.")
    tree_group.add_argument("--payload", action="store_true", help="The element to use for a corpus tag.")

    # If no member of this group is specified, a '1' will be put in the output XML.
    tag_version_group = parser.add_mutually_exclusive_group()
    tag_version_group.add_argument("--tag-version", type=int, help="An integer to use to declare the tag version.")
    tag_version_group.add_argument("--tag-version-file", help="A file containing the integer tag version.")

    parser.add_argument("out_swidtag")

    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG if args.debug else logging.INFO)

    main()
