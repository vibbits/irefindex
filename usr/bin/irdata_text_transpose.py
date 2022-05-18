#!/usr/bin/python3

"""
Transpose input lines, writing fields from each line to separate output lines.

The input tokens are read from a file or stream (depending on the arguments)
employing a tab-separated format (or a format employing a specified delimiter)
where the input tokens are (unless otherwise stated) the only fields on each
line:

<field>...

The output will resemble the following:

<field>
...

Where a start field is specified, preceding fields will not be transposed and
will appear together on every output line derived from a particular input line.

Thus, the input data will resemble the following:

<preceding-field>... <field>...

The corresponding output will resemble this:

<preceding-field>... <field>
<preceding-field>... ...

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
    argparser.add_argument("-f", metavar="start-field", type=int, default=1)
    argparser.add_argument("-t", metavar="end-field", type=int)
    argparser.add_argument("-d", metavar="delimiter", default="\t")
    argparser.add_argument("-w", metavar="delimiter-within-fields", default="\t")
    argparser.add_argument("-s", metavar="sequence-start", type=int)
    argparser.add_argument("filename", help="name of a file or '-'")

    args = argparser.parse_args()

    # treat 1-index as 0-index plus one
    start_field = data.index_for_int(args.f)  # start-field
    end_field = data.int_or_none(args.t)  # end-field
    delimiter = args.d  # delimiter
    delimiter_within_fields = args.w  # delimiter-within-fields
    sequence_start = data.int_or_none(args.s)  # sequence-start

    if args.filename != "-":
        filename_or_stream = args.filename
    else:
        filename_or_stream = data.reread(sys.stdin)

    reader = data.RawImportFileReader(filename_or_stream, delimiter=delimiter)
    writer = data.RawImportFile(data.rewrite(sys.stdout))

    try:
        try:
            for details in reader:

                # Process the data.

                preceding, fields, following = data.partition(
                    details, start_field, end_field
                )

                if delimiter_within_fields != delimiter:
                    split_fields = []
                    for field in fields:
                        split_fields += field.split(delimiter_within_fields)
                    fields = split_fields

                for i, field in enumerate(fields):
                    if sequence_start is not None:
                        values = [i + sequence_start, field]
                    else:
                        values = [field]
                    writer.append(preceding + values + following)

        except IOError as exc:
            print("%s: %s" % (progname, exc), file=sys.stderr)

    finally:
        writer.close()
        reader.close()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(1)

# vim: tabstop=4 expandtab shiftwidth=4
