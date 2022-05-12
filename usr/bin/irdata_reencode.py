#!/usr/bin/python3

"""
Recode the contents of a file, writing a new file with a different encoding to
the original file.

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

if __name__ == "__main__":
    import sys, os, codecs

    progname = os.path.basename(sys.argv[0])

    try:
        infile, outfile, inencoding, outencoding, failencoding = sys.argv[1:6]
    except ValueError:
        print(
            "Usage: %s <input filename> <output filename> <input encoding> <output encoding> <failure encoding>"
            % progname,
            file=sys.stderr,
        )
        sys.exit(1)

    f_in = open(infile)
    f_out = codecs.open(outfile, "w", encoding=outencoding)
    try:
        for lineno, line in enumerate(f_in):
            try:
                uline = str(line, inencoding)
            except UnicodeError:
                print("Encoding error on line %d." % (lineno + 1), file=sys.stderr)
                uline = str(line, failencoding)
            f_out.write(uline)
    finally:
        f_out.close()
        f_in.close()

# vim: tabstop=4 expandtab shiftwidth=4
