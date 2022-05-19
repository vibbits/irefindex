#!/usr/bin/python3

"""
Pad a text file to have a specific number of columns.

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
import os
import sys
from irdata import data


# Main program.


def main():
    progname = os.path.basename(sys.argv[0])

    # Get the command line options.
    argparser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    argparser.add_argument(
        "-n", dest="fields", metavar="fields", required=True, type=int
    )
    argparser.add_argument("-p", dest="padding", metavar="padding", required=True)
    argparser.add_argument(
        "filename", help="name of a file, or '-' [default]", default="-", nargs="?"
    )
    args = argparser.parse_args()

    fields = args.fields
    padding = args.padding

    if args.filename != "-":
        filename_or_stream = args.filename
    else:
        filename_or_stream = data.reread(sys.stdin)

    reader = data.RawImportFileReader(filename_or_stream)
    writer = data.RawImportFile(data.rewrite(sys.stdout))

    try:
        try:
            for details in reader:

                # Pad the line to have at least as many fields as indicated.

                if len(details) < fields:
                    details += (fields - len(details)) * [padding]

                writer.append(details)

        except IOError as exc:
            print("%s: %s" % (progname, exc), file=sys.stderr)

    finally:
        reader.close()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(1)

# vim: tabstop=4 expandtab shiftwidth=4
