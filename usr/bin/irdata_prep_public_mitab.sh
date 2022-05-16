#!/bin/bash

# Copyright (C) 2015 Ian Donaldson <ian@donaldsonresearch.com>
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
Usage: $PROGNAME prepares public mitab from full build by selecting entries from a subset of databases and re-writing them to a folder called public.  MITAB files are automatically detected and processed.

EOF
    exit 1
fi

mkdir public_mitab

#get a unique list of score types
PUBLIC_SOURCES="MI:0462(bind) MI:0463(biogrid) MI:0000(corum) MI:0465(dip) MI:0468(hprd) MI:0469(intact) MI:0917(matrixdb) MI:0000(mpact) MI:0903(mpidb) MI:0000(mppi)"


for FILENAME in *.mitab*.txt; do
head -n 1 $FILENAME > public_mitab/$FILENAME
for PUBLIC_SOURCE in $PUBLIC_SOURCES; do
    echo -e "\n processing $PUBLIC_SOURCE for $FILENAME"
    awk -v public_source=$PUBLIC_SOURCE 'BEGIN {FS="\t"; OFS="\t"}{if($13==public_source) print $0}' < $FILENAME >> public_mitab/$FILENAME
done
done





