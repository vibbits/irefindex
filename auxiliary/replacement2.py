#!/usr/bin/python2
import csv
with open("inputfile", "r") as infile, open("ouputfile", "w") as outfile:
    reader = csv.reader(infile, delimiter="\t")
    writer = csv.writer(outfile, delimiter="\t", quoting=csv.QUOTE_NONE, doublequote= False, quotechar = '')
    for row in reader:
        newdata = str.replace('pattern1','pattern2')
        str = newdata
        writer.writerow(row)