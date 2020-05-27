#!/usr/bin/python2
f = open('file','r')
filedata = f.read()
f.close()
newdata = filedata.replace("pattern1","pattern2")
f = open('file','w')
f.write(newdata)
f.close()

                