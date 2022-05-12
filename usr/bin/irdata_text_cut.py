#!/usr/bin/python3

"""
Cut columns from a file in order of the specified symbolic field names read
from the input file.

--------

Copyright (C) 2011, 2012 Ian Donaldson <ian.donaldson@biotek.uio.no>
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

from irdata.data import (
    RawImportFileReader,
    RawImportFile,
    reread,
    rewrite,
    index_for_int,
)
import os, sys, cmdsyntax

syntax_description = """
    --help |
    (
      [ -f ] <fields>
      [ <filename> | - ]
    )
    """

# Main program.


def main():
    progname = os.path.basename(sys.argv[0])

    # Get the command line options.

    syntax = cmdsyntax.Syntax(syntax_description)
    try:
        matches = syntax.get_args(sys.argv[1:])
        args = matches[0]
    except IndexError:
        print("Syntax:", file=sys.stderr)
        print(syntax_description, file=sys.stderr)
        sys.exit(1)
    else:
        if "help" in args:
            print(__doc__, file=sys.stderr)
            print("Syntax:", file=sys.stderr)
            print(syntax_description, file=sys.stderr)
            sys.exit(1)

    fields = list(map(index_for_int, args["fields"].split(",")))

    if "filename" in args:
        filename = filename_or_stream = args["filename"]
    else:
        filename_or_stream = reread(sys.stdin)
        filename = None

    reader = RawImportFileReader(filename_or_stream)
    writer = RawImportFile(rewrite(sys.stdout))

    try:
        try:
            for details in reader:

                # Filter the fields.

                details = [details[field] for field in fields if field is not None]

                # Cut the columns according to the field details.

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
