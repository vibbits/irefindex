#!/usr/bin/python3

"""
Search an input file using an index file for faster access to specific records.

This program loads an index file and uses bisection to find the closest index
entry in the index for a given search term. It then uses the offset given for
the index entry to seek in the data file, scanning lines in the data file until
it finds the term, stopping if the term is not present.

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

from irdata.data import rewrite, index_for_int
import os, sys, cmdsyntax, bisect


def get_index(f):

    "Return an index stored in the given file 'f'."

    index = []
    for line in f:
        line = line.strip()
        if line:
            term, offset = line.split("\t")
            index.append((term, int(offset)))

    return index


syntax_description = """
    --help |
    (
      <index filename> <data filename> [ -f <field> ] [ -d <separator> ] <term>
    )
    """

if __name__ == "__main__":
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

    # Get the index.

    indexfile = args["index filename"]
    f_index = open(indexfile)

    # Get the data.

    datafile = args["data filename"]
    f_data = open(datafile)

    # Get the field to be treated as the indexed term.

    if "index" in args:
        field = index_for_int(args["index"])
    else:
        field = 0

    # Get the field separator.

    if "separator" in args:
        separator = args["separator"]
    else:
        separator = "\t"

    # Get the search term.

    term = args["term"]

    try:
        index = get_index(f_index)
        writer = rewrite(sys.stdout)

        # Search using a tuple in order to compare correctly with the index.

        i = bisect.bisect_left(index, (term, None))

        if i < len(index):
            term, offset = index[i]
            f_data.seek(offset)

            while 1:
                line = f_data.readline()
                if not line:
                    break

                found = line.split(separator)[field]
                if found >= term:
                    if found == term:
                        writer.write(line)
                    break

    finally:
        f_index.close()
        f_data.close()

# vim: tabstop=4 expandtab shiftwidth=4
