#!/usr/local/bin/python

import sys
import os
import re
import subprocess
import numpy as np
import scipy.io
import matplotlib.pyplot as plt
import pylab

def Usage():
    print '''
Usage: convrg_t.py -h
       convrg_t.py --help
       convrg_t.py <pattern> <acc_thr1> <acc_thr2> <outfile>

           pattern  = regular expression, default is ".*"
           acc_thr  = accuracy threshold, e.g. 0.98

'''
    exit()
    
# Get the total number of args passed
params_total    = len(sys.argv)

if params_total != 5:
    Usage()

else:
    colombe_root = os.environ['COLOMBE_ROOT']
            
    if sys.argv[1] == '-h' or sys.argv[1] == '--help':
        Usage()

    pattern         = sys.argv[1]
    acc_thr1        = float(sys.argv[2])
    acc_thr2        = float(sys.argv[3])
    outfile         = sys.argv[4]
        
    the_cwd = colombe_root + '/exp'
    os.chdir(the_cwd)
    file_list = os.listdir('.')
    file_list.sort()
    
    file_idx        = 0
    prev_line_cnt   = -1    

    flt_re = r'([e\-0-9\.]+)'
    test_flt_str    = "Test.*accuracy = %s" % flt_re
    
    for the_dir in file_list:
        m = re.search( pattern, the_dir )
        
        if m:
            # Get line count of lines matching pattern
            # Add to line_cnt
            sys_cmd = 'grep -P "%s" %s/stdout_log | wc' % (test_flt_str, the_dir)
#            print 'sys_cmd=%s' % sys_cmd
            wc = subprocess.check_output( [sys_cmd], shell=True)
            m = re.search( "^\s*([e\-0-9\.]+)\s", wc )

            line_cnt = int(m.group(1))
            if prev_line_cnt != -1:
                if line_cnt != prev_line_cnt:
                    print "Error: line_cnt=%d, prev_line_cnt=%d" % (line_cnt, prev_line_cnt)
                    exit( 1 )
            prev_line_cnt = line_cnt
            
            file_idx = file_idx + 1    
#            print "%s: %d" % (the_dir, line_cnt)
    
    the_test_arr    = np.ndarray(shape=(line_cnt, file_idx), dtype="i4,f8", order='C')
    the_dir_arr     = []
    file_idx        = 0
    num_bins        = line_cnt + 1
    the_histo       = np.zeros(num_bins)
    iteration       = 0
    iteration_delta = 0
    
    for the_dir in file_list:
        m = re.search( pattern, the_dir )
        
        if m:
            the_dir_arr.append( the_dir )
            fd_src = open( "%s/stdout_log" % the_dir, "r" )
            
            test_row_idx  = 0
            
            rise_start = 0
            
            while ( 1 ):
                x = fd_src.readline()
                if x == "":
#                    print "%s, inf: %f" % (the_dir, the_val)
                    the_histo[num_bins - 1] += 1
                    break
                
                m = re.search( "Iteration ([0-9]+), Testing", x )
                if m:
                    if iteration == 0:
                        iteration_delta = float(m.group(1)) - iteration
                    iteration = float(m.group(1))
                    
                m = re.search( test_flt_str, x )
                if m:
                    the_val = float(m.group(1))
                    the_test_arr[test_row_idx][file_idx]['f0'] = iteration
                    the_test_arr[test_row_idx][file_idx]['f1'] = the_val
                    
                    if the_val >= acc_thr2:
#                        print "%s, %d: %f" % (the_dir, iteration, the_val)
                        if rise_start == 0:
                            the_histo[0] += 1
                        else:
                            # print "iteration=%d, rise_start=%d" % (iteration, rise_start)
                            the_histo[(iteration-rise_start)/iteration_delta] += 1
                        break
                    elif rise_start == 0 and the_val >= acc_thr1:
                        rise_start = iteration
                        
                    test_row_idx = test_row_idx + 1
#                    print "%d %d\n" % (iteration, test_row_idx)
            
            file_idx = file_idx + 1    
            fd_src.close()
    
    print "the_histo = [ ",
    len(the_histo)
    for i in range(num_bins):
        print "%s " % the_histo[i],
    print "];"
    plt.plot(the_histo)
    pylab.show()
