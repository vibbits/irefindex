#!/usr/bin/python3

"""
Reads the (compressed) <file> in swissprot format,
and prints the entry if the entry index % <total> == <rank>

--------

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

import gzip
import pathlib
import re
import typing


def swiss_prot_entry(
    textstream: typing.TextIO, delimiter: typing.Pattern[str] = re.compile(r"^//$")
) -> typing.Generator[str, None, None]:
    """
    Returns the next record from <textstream> as a string.
    SwissProt/UniProt format: https://www.uniprot.org/docs/userman.htm
    """
    lines = list()

    for line in textstream:
        lines.append(line)
        if delimiter.match(line):
            yield "".join(lines)
            lines.clear()


def split_file(filename: pathlib.Path, rank: int, total: int) -> None:
    """
    Splits file with <filename> in individual records.
    If the file is compressed, it id assumed to have extension .gz.

    Records having index % <total> == <rank> are written to stdout, other
    records are simply discarded. For instance, if <total> is 4
    and <rank> is 0, only records #0, #4, #8, #12... are written out.
    """
    opener = gzip.open if filename.endswith(".gz") else open
    with opener(filename, "rt") as stream:
        for n, entry in enumerate(swiss_prot_entry(stream)):
            if n % total == rank:
                print(entry, end="")


if __name__ == "__main__":
    import argparse

    argparser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    argparser.add_argument(
        "filename",
        help="Name of a file, compressed files should have the .gz extension.",
    )
    argparser.add_argument(
        "rank", help="Positive integer, less than <total>.", type=int
    )
    argparser.add_argument("total", help="Positive integer.", type=int)
    args = argparser.parse_args()

    # argument checks
    if args.rank < 0 or args.total < 0:
        raise ValueError("<rank> and <total> should be positive integers.")
    if args.rank >= args.total:
        raise ValueError("<rank> should be less than <total>")

    # meat and bones
    split_file(args.filename, args.rank, args.total)
