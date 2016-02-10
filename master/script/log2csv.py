#!/usr/bin/python

import sys
import os
import re

def Usage():
    print '''
Usage: log2csv.py -h
       log2csv.py --help
       log2csv.py
       log2csv.py <pattern>
           pattern = regular expression, default is ".*"

       With no arguments all defaults are used.
       Pattern must be defined to use other arguments
'''
    exit()
    
# Get the total number of args passed
params_total    = len(sys.argv)

if params_total > 2:
    Usage()

else:
    pattern = ".*"
        
    if params_total > 1:
        if sys.argv[1] == '-h' or sys.argv[1] == '--help':
            Usage()
            
        pattern = sys.argv[1]
        
    the_cwd = os.environ['COLOMBE_ROOT'] + '/exp'
    os.chdir(the_cwd)
    file_list = os.listdir('.')
    file_list.sort()
    
    the_loss=[[0 for j in range(1000)] for i in range(1000)]

    file_idx = 0
    
    for the_dir in file_list:
        m = re.search( pattern, the_dir )
        
        if m:
            print the_dir
            fd_src = open( "%s/stdout_log" % the_dir, "r" )
            
            row_idx = 0
            
            while ( 1 ):
                x = fd_src.readline()
                if x == "":
                    break
                
                m = re.search( "Train\ net\ output.*loss\ =\ ([0-9\.]+)\s", x )
                
                if m:
                    the_val = float(m.group(1))
                    the_loss[row_idx][file_idx] = the_val
                    print "row = %d, col = %d, loss = %f" % (row_idx, file_idx, the_val)
                    row_idx = row_idx + 1
            
            file_idx = file_idx + 1    
            fd_src.close()
            