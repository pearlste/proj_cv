#!/usr/bin/python

#Usage lmdump2jpgs

import sys
import os
import readline
import re

src_file = sys.argv[1]

fd_src = open( src_file, "r" )

while ( 1 ):
    x = fd_src.readline()
    if x == "":
        break
#    print "x=%s\n" % str(x)
    
    m = re.search( "(out_[0-9][0-9][0-9][0-9][0-9]\.jpg)", x )
    
    if m:
        print m.group(1)
#    print "the_line=%s\n" % str(the_line)

    
fd_src.close()
