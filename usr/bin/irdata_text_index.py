#!/usr/bin/python3

"""
Index an input file for faster access to specific records.

This program scans a file and for each line occurring at the given interval,
a value identifying the line and the byte offset of the line is produced.

--------

Copyright (C) 2012 Ian Donaldson <ian.donaldson@biotek.uio.no>
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

import argparse
import gzip
import os
import sys
from irdata import data


if __name__ == "__main__":
    progname = os.path.basename(sys.argv[0])

    # Get the command line options.
    argparser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    argparser.add_argument("-f", dest="field_index", metavar="field-index", type=int)
    argparser.add_argument("-d", dest="separator", metavar="separator", default="\t")
    argparser.add_argument("interval", help="positive number", type=int)
    argparser.add_argument(
        "filename", help="name of a file, or '-' [default]", default="-", nargs="?"
    )
    args = argparser.parse_args()

    # Get the interval.
    interval = args.interval

    # Get the input stream.
    if args.filename != "-":
        infile = args.filename
        leafname = os.path.split(infile)[-1]
        basename, ext = os.path.splitext(leafname)
        if ext.endswith("gz"):
            opener = gzip.open
        else:
            opener = open
        f_in = opener(infile)
    else:
        f_in = sys.stdin

    # Get the field to be treated as the indexed term.
    field = 0 if args.field_index is None else data.index_for_int(args.field_index)
    # Get the field separator.
    separator = args.separator

    try:
        pos = 0
        lineno = 0
        current_value = None
        current_value_start = None
        last_value = None

        writer = data.RawImportFile(sys.stdout)

        while 1:
            line = f_in.readline()
            if not line:
                break

            value = line.split(separator)[field]

            # For new values, remember where they first appeared.

            if value != current_value:
                current_value = value
                current_value_start = pos

            # Emit the start of the current value region.

            if lineno % interval == 0 and current_value != last_value:
                writer.append((current_value, current_value_start))
                last_value = current_value

            lineno += 1
            pos += len(line)

    finally:
        if infile != "-":
            f_in.close()

# vim: tabstop=4 expandtab shiftwidth=4
