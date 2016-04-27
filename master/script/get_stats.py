#!/usr/local/bin/python

import sys
import os
import re
import subprocess
import numpy as np

def Usage():
    print '''
Usage: get_stats.py

            Looks into each directories under $COLOMBE_ROOT/exp, 
            extracts statistics from the file 'stdout_log',
            creates file 'extracted_stats' in each dir under exp
'''
    exit()
    
# Get the total number of args passed
params_total    = len(sys.argv)

if params_total > 2:
    Usage()

else:
    colombe_root = os.environ['COLOMBE_ROOT']
    the_cwd = colombe_root + '/exp'
    os.chdir(the_cwd)

    file_list = os.listdir('.')
    file_list.sort()
    
    file_idx        = 0
    prev_line_cnt   = -1    

    flt_re = r'([e\-0-9\.]+)'

    flt_str_tst_loss = "Test net output.*loss = %s "   % flt_re
    flt_str_trn_loss = "Train net output.*loss = %s "  % flt_re
    flt_str_tst_accu = "Test.*accuracy = %s"           % flt_re
    flt_str_trn_accu = "Train.*accuracy = %s"          % flt_re
    
    for the_dir in file_list:
        iteration       = -1
        iteration_prev  = -1
    
        # Open 'stdout_log' file for reading
        try:
            fd_src = open( "%s/stdout_log" % the_dir, "r" )

        except (OSError, IOError) as e:
            print "\n\n*** Can't find file %s/stdout_log\n\n" % the_dir
            continue

        try:
            dir_exists = 1
            fd_flt_str_tst_loss = open( "%s/tst_loss" % the_dir, "r" )
            
        except (OSError, IOError) as e:
            dir_exists = 0
            print "Note: stats file %s/tst_loss does not exist ..." % the_dir

        if dir_exists:
            print "Note: stats file %s/tst_loss exists ..." % the_dir
            fd_flt_str_tst_loss.close()

        if dir_exists:
            continue
                                    
        # Open stats files for writing
        try:
            fd_flt_str_tst_loss = open( "%s/tst_loss" % the_dir, "w" )
            fd_flt_str_trn_loss = open( "%s/trn_loss" % the_dir, "w" )
            fd_flt_str_tst_accu = open( "%s/tst_accu" % the_dir, "w" )
            fd_flt_str_trn_accu = open( "%s/trn_accu" % the_dir, "w" )

        except (OSError, IOError) as e:
            print "\n\n*** Can't open stats file for writing under %s\n\n" % the_dir
            continue
                                    
        while ( 1 ):
            # Get the next line
            x = fd_src.readline()
            if x == "":
                break
            
            # If the line has Iteration #, then grab it
            m = re.search( "Iteration ([0-9]+)", x )
            if m:
                iteration = int(m.group(1))
                if iteration < iteration_prev:
                    print "*** Error!!!  iteration = %d, iteration_prev=%d\n\n" % (iteration, iteration_prev)
                    exit()
                else:
                    iteration_prev = iteration
                    
            # Check for one of the stats signatures
            m = re.search( flt_str_tst_loss, x )
            if m:
                if iteration < 0:
                    print "*** Error!!!  Iteration = %d\n\n" % iteration
                    exit()
                the_val = float(m.group(1))
                fd_flt_str_tst_loss.write( "%d %f\n" % (iteration, the_val) )
        
            # Check for one of the stats signatures
            m = re.search( flt_str_tst_accu, x )
            if m:
                if iteration < 0:
                    print "*** Error!!!  Iteration = %d\n\n" % iteration
                    exit()
                the_val = float(m.group(1))
                fd_flt_str_tst_accu.write( "%d %f\n" % (iteration, the_val) )
        
            # Check for one of the stats signatures
            m = re.search( flt_str_trn_loss, x )
            if m:
                if iteration < 0:
                    print "*** Error!!!  Iteration = %d\n\n" % iteration
                    exit()
                the_val = float(m.group(1))
                fd_flt_str_trn_loss.write( "%d %f\n" % (iteration, the_val) )
        
            # Check for one of the stats signatures
            m = re.search( flt_str_trn_accu, x )
            if m:
                if iteration < 0:
                    print "*** Error!!!  Iteration = %d\n\n" % iteration
                    exit()
                the_val = float(m.group(1))
                fd_flt_str_trn_accu.write( "%d %f\n" % (iteration, the_val) )
        
        
        fd_src.close()
        fd_flt_str_tst_loss.close()
        fd_flt_str_trn_loss.close()
        fd_flt_str_tst_accu.close()
        fd_flt_str_trn_accu.close()
        
