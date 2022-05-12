#!/usr/bin/python3

"""
Extract term information from the PSI-MI ontology file, producing a file with
the following structure:

<identifier> <name> (preferred|synonym) <qualifier>

The qualifier may be given as an encoded null value ("\N") for synonyms and is
always null for preferred names.

--------

Copyright (C) 2012, 2013 Ian Donaldson <ian.donaldson@biotek.uio.no>
Original author: Paul Boddie <paul.boddie@biotek.uio.no>

This program is free software; you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation; either version 3 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import re

#                              synonym: "name"  EXACT qualifier   []
synonym_pattern = re.compile(r'synonym: "(.*?)" EXACT (?:(.*?) )?\[\]')

def parse(infile, outfile):
    state = None
    id = None

    line = infile.readline()

    while line:
        line = line.rstrip('\r\n')

        if line.startswith("[Term]"):
            state = "TERM"

        elif state == "TERM" and line.startswith("id: "):
            state = "ID"
            id = line[4:]

        elif state == "ID":
            if line.startswith("name: "):
                output = [id, line[6:], 'preferred', "\\N"]
                print("\t".join(output), file=outfile)
            else:
                match = synonym_pattern.match(line)
                if match:
                    output = [id, match.group(1), 'synonym', match.group(2) or "\\N"]
                    print("\t".join(output), file=outfile)

        elif not line.strip():
            state = None

        line = infile.readline()

if __name__ == "__main__":
    from os.path import join, split
    import os, sys

    progname = os.path.basename(sys.argv[0])

    try:
        i = 1
        data_directory = sys.argv[i]
        filename = sys.argv[i+1]
    except IndexError:
        print("Usage: %s <output data directory> <data file>" % progname, file=sys.stderr)
        sys.exit(1)

    try:
        leafname = split(filename)[-1]

        if filename == "-":
            print("%s: Parsing standard input" % progname, file=sys.stderr)
            f = sys.stdin
        else:
            print("%s: Parsing %s" % (progname, leafname), file=sys.stderr)
            f = open(filename)

        f_out = open(join(data_directory, "terms"), "w")

        try:
            parse(f, f_out)
        finally:
            if filename != "-":
                f.close()
            f_out.close()

    except Exception as exc:
        print("%s: Parsing failed with exception: %s" % (progname, exc), file=sys.stderr)
        sys.exit(1)

# vim: tabstop=4 expandtab shiftwidth=4
