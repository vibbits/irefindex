#!/bin/sh

# Copyright (C) 2015 Ian Donaldson <ian@donaldsonresearch.com>
# Original author: Ian Donaldson <ian@donaldsonresearch.com>

if [ -e "irdata-config" ]; then
    . "$PWD/irdata-config"
elif [ -e "scripts/irdata-config" ]; then
    . 'scripts/irdata-config'
else
    . 'irdata-config'
fi

DATESTAMP=`date +%m-%d-%Y`
MITAB_COMPLETE_OUTPUT="$DATA/All.mitab.$DATESTAMP.txt"
MITAB_ORGANISM_OUTPUT="$DATA/{}.mitab.$DATESTAMP.txt"

if [ "$1" = '--help' ]; then
    cat 1>&2 <<EOF
Usage: $PROGNAME 

Generate iRefPro tables and export tables as text.  There are no options.

EOF
    exit 1
fi

echo $DATA
echo $DATABASE
echo $SQL
echo $PSQL_OPTIONS
echo `whoami`

if ! "$TOOLS/irdata_database_action.py" "$DATABASE" "$SQL/export_irefpro.sql" "$DATA" $PSQL_OPTIONS ; then
    echo "$PROGNAME: Could not generate iRefPro data." 1>&2
    exit 1
fi


