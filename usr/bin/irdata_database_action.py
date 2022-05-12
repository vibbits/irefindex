#!/usr/bin/python3

"""
Perform operations on a relational database system using templates.

--------

Copyright (C) 2009, 2010, 2011, 2012 Ian Donaldson <ian.donaldson@biotek.uio.no>
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

import os, tempfile
import subprocess


def substitute(s, defs):
    for name, value in list(defs.items()):
        s = s.replace("<%s>" % name, value)
    return s


def execute_command(cmd, database_name, psql_options=None):
    fd, cmd_filename = tempfile.mkstemp()
    try:
        fc = os.fdopen(fd, "w")
        try:
            fc.write(cmd)
        finally:
            fc.close()
        if subprocess.call(
            ["psql"]
            + (psql_options or [])
            + ["-v", "ON_ERROR_STOP=true", "-f", cmd_filename, database_name]
        ):
            sys.exit(1)
    finally:
        os.remove(cmd_filename)


if __name__ == "__main__":
    import sys, os

    progname = os.path.basename(sys.argv[0])

    if len(sys.argv) < 3:
        print(
            "Usage: %s ( <database> | --output-command )"
            " <template> [ <data_directory> ]"
            " [ --psql-options ... ]"
            " [ --defs ( <name> <value> ) ... ]" % progname,
            file=sys.stderr,
        )
        sys.exit(1)

    database_name = sys.argv[1]
    template = sys.argv[2]
    d, filename = os.path.split(sys.argv[0])
    output_command = database_name == "--output-command"

    try:
        psql_options_start = sys.argv.index("--psql-options")
    except ValueError:
        psql_options_start = None

    try:
        defs_start = sys.argv.index("--defs")
    except ValueError:
        defs_start = None

    if len(sys.argv) > 3 and defs_start != 3 and psql_options_start != 3:
        data_directory = sys.argv[3]
    else:
        data_directory = "data"

    if psql_options_start is not None:
        psql_options = sys.argv[psql_options_start + 1 : defs_start]
    else:
        psql_options = []

    defs = {}
    if defs_start is not None:
        for i in range(defs_start + 1, len(sys.argv), 2):
            defs[sys.argv[i]] = sys.argv[i + 1]

    defs["directory"] = os.path.abspath(data_directory)

    f = open(template)
    try:
        cmd = f.read()
        cmd = substitute(cmd, defs)
        if output_command:
            print(cmd)
        else:
            execute_command(cmd, database_name, psql_options)
    finally:
        f.close()

# vim: tabstop=4 expandtab shiftwidth=4
