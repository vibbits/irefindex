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
Usage: $PROGNAME path_to_mitab_file 

Check the morphology of a mitab file. Each column is examined in succession. The head and tail are shown and 
a selected list of the 20 or 30 most commonly occurring values for that field (or the types of values for that field)
is displayed along with the counts for the number of times observed.  The output is meant to be human inspected for
anomolies.

EOF
    exit 1
fi


MITAB_FILE=$1

#check that a file has been specified
if [ ! "$MITAB_FILE" ] || [ ! -f "$MITAB_FILE" ]; then
	#quit
        echo "cannot open file $MITAB_FILE"
        exit 1
fi

#check that the file has correct number of columns
echo -e 'checking number of rows and columns\n'
echo -e 'rows\tcolumns'
awk 'BEGIN {FS="\t";}{print NF}' $MITAB_FILE | sort | uniq -c

#print out the column headings for inspection
echo -e '\nchecking column header\n'
head -n 1 $MITAB_FILE | t2r


#cycle through all columns and examine
for i in `seq 1 54`;
do
    #print out head and tail for inspection
    echo -e "\n********************"
    echo -e "examining column $i\n"
    cut -f $i $MITAB_FILE | head
    echo -e '\ntail\n'
    tail $MITAB_FILE | cut -f $i 
    #examine counts of different entry types for various fields 
    #the code below is fairly repetitive intentionally to leave placeholders for 
    #adding new methods to examine column contents
    #
    #uids
    if [ "$i" -eq 1 -o "$i" -eq 2 ]; then
        echo -e '\ncount\tentry type'
        cut -f $i $MITAB_FILE | cut -f 1 -d ':' | sort | uniq -c | sort -nr
    fi        
    #alternate names
    if [ "$i" -eq 3 -o "$i" -eq 4 ]; then
        echo -e '\ncount\tentry type - for first entry only' 
        cut -f $i $MITAB_FILE | cut -f 1 -d ':' | sort | uniq -c | sort -nr
    fi
    #examine counts of different entry types for aliases
    if [ "$i" -eq 5 -o "$i" -eq 6 ]; then
        echo -e '\ncount\tentry type - for first entry only' 
        cut -f $i $MITAB_FILE | cut -f 1 -d ':' | sort | uniq -c | sort -nr
    fi
    #examine counts of different entry types for methods
    if [ "$i" -eq 7 ]; then
        echo -e '\ncount\tvalue type - all method entry types shown' 
        cut -f $i $MITAB_FILE | sort | uniq -c | sort -nr
    fi
    #examine counts of different entry types for authors
    if [ "$i" -eq 8 ]; then
        echo -e '\ncount\tvalue type - top 30 only' 
        cut -f $i $MITAB_FILE | sort | uniq -c | sort -nr | head -n 30
    fi
    #examine counts of different entry types for pmids
    if [ "$i" -eq 9 ]; then
        echo -e '\ncount\tentry type' 
        cut -f $i $MITAB_FILE | cut -f 1 -d ':' | sort | uniq -c | sort -nr 
        echo -e '\ncount\tentry type - top 30 only' 
        cut -f $i $MITAB_FILE | cut -f 2 -d ':' | sort | uniq -c | sort -nr | head -n 30
    fi
    #examine counts of different entry types for taxons
    if [ "$i" -eq 10 -o "$i" -eq 11 ]; then
        echo -e '\ncount\tentry type' 
        cut -f $i $MITAB_FILE | cut -f 1 -d ':' | sort | uniq -c | sort -nr 
        echo -e '\ncount\tentry type - top 30 only' 
        cut -f $i $MITAB_FILE | cut -f 2 -d ':' | sort | uniq -c | sort -nr | head -n 30
    fi
    #examine counts of different entry types for interaction types
    if [ "$i" -eq 12 ]; then
        echo -e '\ncount\tvalue type - all interaction-type entry types shown' 
        cut -f $i $MITAB_FILE | sort | uniq -c | sort -nr
    fi
    #examine counts of different entry types for source database
    if [ "$i" -eq 13 ]; then
        echo -e '\ncount\tvalue type - all source database entry types shown' 
        cut -f $i $MITAB_FILE | sort | uniq -c | sort -nr
    fi
    #examine counts of different entry types for interaction identifiers
    if [ "$i" -eq 14 ]; then
        echo -e '\ncount\tentry type - only for first entry in pipe-delimited list' 
        cut -f $i $MITAB_FILE | cut -f 1 -d ':' | sort | uniq -c | sort -nr
        echo -e '\ncount\texpansion type - third entry in pipe-delimited list' 
        cut -f $i $MITAB_FILE | cut -f 3 -d '|' | sort | uniq -c | sort -nr    
    fi
    #examine counts of different entry types for confidence
    if [ "$i" -eq 15 ]; then
        echo -e '\ncount\tlpr score type - second entry in pipe-delimited list - top 20 only' 
        cut -f $i $MITAB_FILE | cut -f 2 -d '|' | sort | uniq -c | sort -nr | head -n 20
        echo -e '\ncount\tnp score type - third entry in pipe-delimited list - top 20 only' 
        cut -f $i $MITAB_FILE | cut -f 3 -d '|' | sort | uniq -c | sort -nr | head -n 20
    fi
    #examine counts of different entry types for expansion
    if [ "$i" -eq 16 ]; then
        echo -e '\ncount\texpansion type - all types shown' 
        cut -f $i $MITAB_FILE | sort | uniq -c | sort -nr
    fi
    #examine counts of different entry types for 
    #biological role A and B, 
    #experimental role A and B,
    #interactor type A and B
    #xrefs A, B and I
    #annotation A, B and I
    #host organism
    #parameters
    #creation date
    #update date
    if [ "$i" -gt 16 -a "$i" -lt 33 ]; then
        echo -e '\ncount\tvalue type - top 20 only' 
        cut -f $i $MITAB_FILE | sort | uniq -c | sort -nr | head -n 20
    fi
    #checksum A, B and I
    #negative
    if [ "$i" -gt 32 -a "$i" -lt 37 ]; then
        echo -e '\ncount\tentry type' 
        cut -f $i $MITAB_FILE | cut -f 1 -d ':' | sort | uniq -c | sort -nr | head -n 20
    fi
    #original reference A and B
    #final reference A and B
    #mapping score A and B
    #irogid A and B
    #irigid
    #crogid A and B
    #crigid
    #icrogid A and B
    #icrigid
    #imexid
    #edgetype
    #numParticipants
    if [ "$i" -gt 36 -a "$i" -lt 55 ]; then
        echo -e '\ncount\tvalue type or entry type - top 20 only' 
        cut -f $i $MITAB_FILE | cut -f 1 -d ':' | sort | uniq -c | sort -nr | head -n 20
    fi    



done

echo -e "\nfinished\n"

