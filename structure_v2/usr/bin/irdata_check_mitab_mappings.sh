#!/bin/sh

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
Usage: $PROGNAME path_to_mitab_file number_of_sample_lines limit_to_source

e.g. irdata_check_mitab_mappings.sh All.mitab.123456.txt 5 BIND

Retrieve a random sampling of interactor mappings for each distinct mapping score.  The output is meant to be human inspected for anomolies.

EOF
    exit 1
fi


MITAB_FILE=$1
N_SAMPLELINES=$2


#check that a file has been specified
if [ ! "$MITAB_FILE" ] || [ ! -f "$MITAB_FILE" ]; then
	#quit
        echo "cannot open file $MITAB_FILE"
        exit 1
fi
if [ ! "$N_SAMPLELINES" ]; then
	N_SAMPLELINES=5
fi


#get a unique list of score types
ALL_SCORES="$(cut -f 41 $MITAB_FILE | sort | uniq)"
#remove - and column header
ALL_SCORES=${ALL_SCORES//-/ }
ALL_SCORES=${ALL_SCORES//MappingScoreA/ }


for SCORE in $ALL_SCORES; do
    echo -e "\n" $SCORE
    echo -e "score\toriginal\tfinal\tuid\ttaxid\tsourcedb\tinteractionIdentifier"
    awk -v score=$SCORE 'BEGIN {FS="\t"; OFS="\t"}{if($41==score ) print $41,$37,$39,$1,$10,$13,$14}' < $MITAB_FILE| head -n $N_SAMPLELINES
done

#selecting a random line from a file using mapfile
#mapfile -s 42 -n 3 < All.mitab.04-07-2015.txt 
#printf '%s' "${MAPFILE[2]}"
#or
#echo "${MAPFILE[2]}"

#grep $SCORE All.mitab.04-07-2015.txt | mapfile -s 42 -n 3 MAPFILE
#echo




