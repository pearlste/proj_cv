#!/usr/bin/python

#Usage rem_to_left_of_sqr_brack

import sys
import os
import readline

print "%d params\n\n" % len(sys.argv)

src_file = sys.argv[1]
dst_file = sys.argv[2]

src_file
dst_file

fd_src = open( src_file, "r" )
fd_dst = open( dst_file, "w" )

while ( 1 ):
    x = fd_src.readline()
    if x == "":
        break
#    print "x=%s\n" % str(x)
    
    the_line = x.split( "]", 1 )
#    print "the_line=%s\n" % str(the_line)

    if len(the_line) > 1:
        fd_dst.write(the_line[1])
    
fd_src.close()
fd_dst.close()
