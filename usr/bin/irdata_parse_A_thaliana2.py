#!/usr/bin/python3

"""
Parse the table embedded in the UniProt FlyBase and Yeast text files.

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

import re

class Parser:

    "A parser for UniProt Arabidopsis  format text files."

    NULL = r"\N"
    NO_RECORD, CONTINUE, END = 0, 1, 2
    column_pattern = re.compile(r"\s+")

    def __init__(self, f, f_out, f_log, filetype, discard_ill_formed, progname):
        self.f = f
        self.f_out = f_out
        self.f_log = f_log
        self.filetype = filetype
        self.discard_ill_formed = discard_ill_formed
        self.progname = progname
        self.columns = None
        self.lineno = None

    def split_line(self, line):
        return self.column_pattern.split(line)

    def get_specified(self, values):
        return len([value for value in values if value])

    def get_values(self, line, continuation=None):

        # Split the line into columns and determine whether a record is present.

        values = self.split_line(line)
        specified = self.get_specified(values)

        # If the boundaries between cells contain text, the end of the table may
        # have been reached.
        """
        boundaries = self.split_line(line, self.boundaries)
        overflows = self.get_specified(boundaries)


        if overflows:
            self.write_log("SERIOUS", "Table cell overflow occurred.")
            if self.discard_ill_formed:
                return None, self.NO_RECORD
        """

        if not continuation and specified < 2:
            return None, self.NO_RECORD

        # Handle compound columns in Arabidopsis.

        if self.filetype == "Arabidopsis_thaliana":
            if values[4] == "Uniprot/SWISSPROT":
                self.write_record(values)
            return None, self.END
        else:
            return None, self.END

    def parse(self):
        values = None
        for self.lineno, line in enumerate(self.f):
            line = line.rstrip("\n")

            # Get the column dimensions.
            """
            if not self.columns:
                if line.startswith("gene_stable_id"):
                    print >>sys.stderr, "puntvier"
                    self.init_columns(line)

            # With column dimensions, get values and the status of each record
            # as new lines are read.

            else:"""
            values, status = self.get_values(line, values)

    def write_record(self, record):
        self.f_out.write("\t".join(record) + "\n")

    def write_log(self, level, message):
        self.f_log.write(
            "%s (%s): %d: %s: %s\n"
            % (self.progname, self.filetype, self.lineno, level, message)
        )


if __name__ == "__main__":
    import os
    import sys

    progname = os.path.basename(sys.argv[0])

    try:
        filetype = sys.argv[1]
        discard_ill_formed = "--discard-ill-formed" in sys.argv
    except IndexError:
        print(
            "Usage: %s ( fly | yeast ) [ --discard-ill-formed ]" % progname,
            file=sys.stderr,
        )
        sys.exit(1)

    try:
        parser = Parser(
            sys.stdin, sys.stdout, sys.stderr, filetype, discard_ill_formed, progname
        )
        parser.parse()
        print("done", file=sys.stderr)
    except Exception as exc:
        print(
            "%s: Parsing failed with exception: %s" % (progname, exc), file=sys.stderr
        )
        sys.exit(1)

# vim: tabstop=4 expandtab shiftwidth=4
