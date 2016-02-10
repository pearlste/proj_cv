#!/usr/bin/python

import sys
import os
import re

# Usage cstat <pattern> [-l] [n]

def Usage():
    print '''
Usage: cstat.py -h
       cstat.py --help
       cstat.py
       cstat.py <pattern> [-l] [n]
           pattern = regular expression, default is ".*"
           -l = show loss (default is accuracy)
           n  = # of entries per exp (default is 3)
       
       With no arguments all defaults are used.
       Pattern must be defined to use other arguments
'''
    exit()
    
# Get the total number of args passed
params_total    = len(sys.argv)

if params_total > 4:
    Usage()

else:
    pattern = ".*"
    n = 3
    do_loss = 0
    do_acc  = 1
        
    if params_total > 1:
        if sys.argv[1] == '-h' or sys.argv[1] == '--help':
            Usage()
            
        pattern = sys.argv[1]
        
    if params_total > 2:
        if sys.argv[2] == '-l':
            do_loss = 1
            do_acc  = 0
            
            if params_total > 3:
                n = int(sys.argv[3])
        else:
            if params_total > 3:
                Usage()
            else:
                n = int(sys.argv[2])
            
    the_cwd = os.environ['COLOMBE_ROOT'] + '/exp'
    os.chdir(the_cwd)
    file_list = os.listdir('.')
    file_list.sort()
    
    if do_acc:
        for the_dir in file_list:
            m = re.search( pattern, the_dir )
            
            if m:
                print
                print the_dir + ":"
                os.system( 'grep "accuracy =" %s/stdout_log | tail -%d' % (the_dir, n) )
    
    if do_loss:
        for the_dir in file_list:
            m = re.search( pattern, the_dir )
            
            if m:
                print
                print the_dir + ":"
                os.system( 'grep "Iteration.*loss =" %s/stdout_log | tail -%d' % (the_dir, n) )

    print
    