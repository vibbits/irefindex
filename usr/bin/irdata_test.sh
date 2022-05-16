#!/bin/bash

# Copyright (C) 2011-2013 Ian Donaldson <ian.donaldson@biotek.uio.no>
# Original author: Ian Donaldson<ian.oslo@gmail.com>
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

#notes:
#preprocess release 9 file using
#sed s/InnateDB:/innatedb:IDB-/ <All.mitab.10182011.txt > release9.mitab
#before running this script



#######################
# read in env varibales
#######################
if [ -e "irdata-config" ]; then
    . "$PWD/irdata-config"
elif [ -e "scripts/irdata-config" ]; then
    . 'scripts/irdata-config'
else
    . 'irdata-config'
fi

###############
#help and usage
###############
if [ "$1" = '--help' ]; then
    cat 1>&2 <<EOF
Usage: $PROGNAME <mitab-1-filepath> <mitab-2-filepath>

Test general syntax and contents of a MITAB file with respect
to one another.
EOF
    exit 1
fi

#############
# check usage
#############
MITABPATH1=$1
MITABPATH2=$2


if [ ! "$MITABPATH1" ] || [ ! "$MITABPATH2" ]; then
    echo "$PROGNAME: Enter paths to two MITAB files separated by a space." 1>&2
    exit 1
fi

if [ ! -e "$MITABPATH1" ]
then
    echo "$PROGNAME: $MITABPATH1 does not exist." 1>&2
    exit 1
elif [ ! -e "$MITABPATH2" ]
then
    echo "$PROGNAME: $MITABPATH2 does not exist." 1>&2
    exit 1
fi

MITAB1=`basename "$MITABPATH1"`
MITAB2=`basename "$MITABPATH2"`

echo "The first file is $MITAB1"
echo "The second file is $MITAB2"
echo -e "\n\n"

INFILES=("$MITABPATH1 $MITABPATH2")


########
#time check
########
source timer.sh
echo -n "$PROGNAME STARTING "; date
t=$(timer)


################################
echo "Checking number of lines:"
################################

echo -e "$MITAB1\t$MITAB2"
echo -e `cat "$MITABPATH1" | wc -l` "\t" `cat $MITABPATH2 | wc -l`
echo

#############################
echo "Checking columns names"
#############################

COLNAMES1=(`head -n1 "$MITABPATH1"`)
COLNAMES2=(`head -n1 "$MITABPATH2"`)
i=0
j=${#COLNAMES1[@]}
k=${#COLNAMES2[@]}
while [ $i -lt $j ]; do
    if [ "${COLNAMES1[$i]}" == "${COLNAMES2[$i]}" ]; then
        ISOK="OK"
    else
	ISOK="WARNING"
    fi
    printf "%25s %25s %10s\n" "${COLNAMES1[$i]}" "${COLNAMES2[$i]}" "$ISOK"
    #echo -e ${COLNAMES1[$i]} "\t" ${COLNAMES2[$i]}
    ((i++))
    #i=`expr $i + 1`
done


#################
echo "examining two files for number of bind distinct record ids, lines describing bind complexes, irigids for binary ints and complexes"
################

#:<<'SKIPTHIS'
for THISFILE in $INFILES; do
    echo "for $THISFILE"
    echo
    echo "distinct bind ids for all records involving a ppi"
    cut -f 13,14,21,22 $THISFILE | grep 'MI:0462(bind)'|grep 'MI:0326.*MI:0326'|cut -f 2|cut -f 1 -d '|'|sort -u|wc -l
    echo
    echo "distinct bind ids for all records involving a complex"
    cut -f 13,14,21,22 $THISFILE | grep 'MI:0462(bind)'|grep 'MI:0315'|cut -f 2|cut -f 1 -d '|'|sort -u|wc -l
    echo
    echo "distinct irigids (column 45) for all bind records involving a ppi"
    cut -f 13,14,21,22,45 $THISFILE | grep 'MI:0462(bind)'|grep 'MI:0326.*MI:0326'|cut -f 5|sort -u|wc -l
    echo
    echo "distinct irigids (column 45) for all bind records involving a complex"
    cut -f 13,14,21,22,45 $THISFILE | grep 'MI:0462(bind)'|grep 'MI:0315'|cut -f 5|sort -u|wc -l
    echo
done
#SKIPTHIS


function process()
{
    DB=$1
    case $DB in
        bind )
            GREPDB='MI:0462(bind)'
            IDCOL=1;;
        innatedb )
            GREPDB='MI:\<[0-9]\{4\}\>(innatedb)'
            IDCOL=1;;
        mppi )
            GREPDB='MI:\<[0-9]\{4\}\>(mppi)'
            IDCOL=2;;
        matrixdb )
            GREPDB='MI:\<[0-9]\{4\}\>(matrixdb)'
            IDCOL=2;;
        mint )
            GREPDB='MI:0471(mint)'
            IDCOL=2;;
        * )
            GREPDB='NOTFOUND'
            IDCOL=1;;
    esac

    #select db records that describe protein-protein ints and retrieve the db ids for these int records, sorted and unique
    cut -f 13,14,21,22 "$MITABPATH1" | grep -i $GREPDB | grep 'MI:0326.*MI:0326' | cut -f 2 | cut -f $IDCOL -d '|' | sort -u > file.1.$DB
    cut -f 13,14,21,22 "$MITABPATH2" | grep -i $GREPDB | grep 'MI:0326.*MI:0326' | cut -f 2 | cut -f $IDCOL -d '|' | sort -u > file.2.$DB

    echo; echo "finding missing/new/common records for db $DB"

    #create separate files of record identifiers for records that are missing, new or common to the two releases
    #missing

    OUTFILE="$DB-records-missing-from-file-2"
    comm -23 file.1.$DB file.2.$DB > $OUTFILE
    echo -n "$OUTFILE :" ; wc -l $OUTFILE

    echo "Example $DB records missing from current release";echo
    COLNAMES1=(`head -n1 "$MITABPATH1"`)
    COLNAMES2=(`head -n1 "$MITABPATH2"`)

    lno=0
    while read THISACC; do
        ((lno++))
        FULL_EXAMPLE_RECORDS=5
        if [ $lno -lt $FULL_EXAMPLE_RECORDS ]; then
            IFS=$'\t'
            THISRECORD=(`tail -n +2 $MITABPATH1 | grep $THISACC\|`)
            i=0
            j=${#COLNAMES1[@]}
            k=${#THISRECORD[@]}
            while [ $i -lt $j ]; do
                printf "%25s %-.50s\n" "${COLNAMES1[$i]}" "${THISRECORD[$i]}"
                ((i++))
            done
            echo
        fi

        #print out detailed record contents to file
        SHORT_EXAMPLE_RECORDS=100
        if [ $lno -lt $SHORT_EXAMPLE_RECORDS ]; then
            tail -n +2 $MITABPATH1 | grep $THISACC\| | cut -f 14,37,38,39,40,41,42 >> example.missing.$DB
            echo >> example.missing.$DB
        fi
    done < $OUTFILE
    echo "total records found $lno"
    echo;echo

    #new records
    OUTFILE="$DB-records-new-to-file-2"
    comm -13 file.1.$DB file.2.$DB > $OUTFILE
    echo;echo -n $OUTFILE ":" ; wc -l $OUTFILE

    #common records
    OUTFILE="$DB-records-in-both-files"
    comm -12 file.1.$DB file.2.$DB > $OUTFILE
    echo;echo -n $OUTFILE ":" ; wc -l $OUTFILE

    lno=0
    while read THISACC; do
        ((lno++))
        FULL_EXAMPLE_RECORDS=20
        if [ $lno -le $FULL_EXAMPLE_RECORDS ]; then
            IFS=$'\t'
            unset THISRECORD1
            unset THISRECORD2
            THISRECORD1=(`tail -n +2 $MITABPATH1 | grep $GREBDB.*$THISACC\|`)
            THISRECORD2=(`tail -n +2 $MITABPATH2 | grep $GREPDB.*$THISACC\|`)
	    i=0
            j=${#COLNAMES1[@]}
            k=${#THISRECORD[@]}
            while [ $i -lt $j ]; do
                if [ "${THISRECORD1[$i]}" != "${THISRECORD2[$i]}" ]; then ISDIFF="DIFFCOL-$i" ; else ISDIFF=" "; fi
                printf "%25s \t %-.50s \t %-.50s \t %-.10s\n" "${COLNAMES1[$i]}" "${THISRECORD1[$i]}" "${THISRECORD2[$i]}" "$ISDIFF" >> common.records.$DB
                ((i++))
            done
            echo >> common.records.$DB
        fi
    done < $OUTFILE
    echo "total records found $lno"
    echo;echo
}


#for DB in bind innatedb mint mppi matrixdb
for DB in bind
do

    process $DB

done


########
#time check
########
echo -n "$PROGNAME ENDING "; date
printf 'ELAPSED TIME: %s\n' $(timer $t)




#################
#multi line comment
#################
: <<'ENDOFTHEWORLD'
#nothing from here to end will be executed



##################################
echo "Checking general morphology"
##################################

INFILES=("$MITABPATH1 $MITABPATH2")
for INFILE in $INFILES; do
    echo "Examining $INFILE";echo
    lno=0
    while read -a line; do
        ((lno++))
    done < $INFILE
    echo "total lines found $lno"
done
echo;echo



###################
#fodder
###################

#for i in `head -n1 "$MITABPATH1"`;do
#    echo $i
#done

#echo "Distribution of column numbers for all lines in each file."
#http://www.gnu.org/software/gawk/manual/gawk.html
#echo -e "$MITAB1:\nlines\tcolumns"
#awk '{FS="\t";print NF}' "$MITABPATH1" | sort -n | uniq -c
#echo -e "$MITAB2:\nlines\tcolumns"
#awk '{FS="\t";print NF}' "$MITABPATH2" | sort -n | uniq -c
#echo
#echo

#################
#multi line comment
#################


ENDOFTHEWORLD
