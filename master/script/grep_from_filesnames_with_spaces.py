#!/usr/bin/python

import fileinput
import sys
import os
import re

tgt_str = sys.argv[1]

for line in sys.stdin:
    m = re.search( "(.*)", line )
    
    if m:
        filename = m.group(1)

        with open(m.group(1), "r") as myfile:
            fn_yet = 0
            for line in myfile:
                        
                m = re.search( "(%s)"%tgt_str, line )
                if m:
                    if not fn_yet:
                        print filename
                        fn_yet = 1
                    print "    %s"%m.group(1)