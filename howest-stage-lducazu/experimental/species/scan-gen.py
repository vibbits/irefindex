#!/usr/bin/python3
"""
Render jinja template provided a list of species names.

The list of species scientific names is passed to the template as 'names' (a list).
This list is potentially big
"""

import jinja2
import psycopg2
import re


def RenderString(tmpl, db, esc):
    taxonomy_stmt = (
        "select distinct name from taxonomy_names"
        " where nameclass = 'scientific name'"
        " order by name"
        " limit 8000"
    )
    scan_template = jinja2.Template(tmpl)

    with psycopg2.connect(f"dbname={db}") as conn:
        with conn.cursor() as cursor:
            cursor.execute(taxonomy_stmt)
            if esc:
                names = [re.escape(name[0]) for name in cursor]
            else:
                names = [name[0] for name in cursor]

            print(scan_template.render({"names": names}))


def RenderFile(filename, db, esc):
    with open(filename) as fd:
        RenderString(fd.read(), db, esc)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Render jinja template provided a list of species names."
    )
    parser.add_argument(
        "-d", dest="db", default="irdata19", help="name of the pg database"
    )
    parser.add_argument(
        "-n",
        dest="esc",
        action="store_false",
        help="don't escape regex metacharacters",
    )
    parser.add_argument(
        "-t", dest="template", required=True, help="name of the jinja template"
    )
    args = parser.parse_args()

    RenderFile(args.template, args.db, args.esc)
