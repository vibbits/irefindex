#!/bin/bash

# Copyright (C) 2012, 2013 Ian Donaldson <ian.donaldson@biotek.uio.no>
# Original author: Paul Boddie <paul.boddie@biotek.uio.no>
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 3 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.

if [ -e "irdata-config" ]; then
    . "$PWD/irdata-config"
elif [ -e "scripts/irdata-config" ]; then
    . 'scripts/irdata-config'
else
    . 'irdata-config'
fi

if [ "$1" = '--help' ]; then
    cat 1>&2 <<EOF
Usage: $PROGNAME <output data directory> <filename>...

Process the GenPept files (typically in FASTA format), producing data suitable
for iRefIndex in the output data directory.
EOF
    exit 1
fi

DATADIR=$1
shift 1

FILENAMES=$*

if [ ! "$DATADIR" ] || [ ! "$FILENAMES" ]; then
    echo "$PROGNAME: A data directory and input filenames must be specified." 1>&2
    exit 1
fi

  "$SCRIPTS/argument-per-line" $FILENAMES \
| "$SCRIPTS/irparallel" "\"$TOOLS/irdata_parse_fasta.py\" 'GENPEPT' \"$DATADIR\" 'acc,name,organism' 'acc,name,organism' {}"


# Concatenate the output data²
# Tab character used in the sed command.
#TAB=`printf '\t'`

rm -f "$DATADIR/genpept_proteins.txt"
cat "$DATADIR"/*_proteins.txt > "$DATADIR/genpept_proteins.txt"

"$TOOLS/irdata_process_signatures.sh" "$DATADIR" --append --append-length
exit $?
