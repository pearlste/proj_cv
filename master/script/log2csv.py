#!/usr/local/bin/python

import sys
import os
import re
import subprocess
import numpy as np

def Usage():
    print '''
Usage: log2csv.py -h
       log2csv.py --help
       log2csv.py <csv_filename>
       log2csv.py <pattern>  <csv_filename>
           pattern = regular expression, default is ".*"

       With no arguments all defaults are used.
       Pattern must be defined to use other arguments
'''
    exit()
    
# Get the total number of args passed
params_total    = len(sys.argv)

if params_total < 2 or params_total > 3:
    Usage()

else:
    if sys.argv[1] == '-h' or sys.argv[1] == '--help':
        Usage()

    pattern = ".*"
        
    if params_total == 2:
        csv_filename    = sys.argv[1]
    else:
        pattern         = sys.argv[1]
        csv_filename    = sys.argv[2]
        
    the_cwd = os.environ['COLOMBE_ROOT'] + '/exp'
    os.chdir(the_cwd)
    file_list = os.listdir('.')
    file_list.sort()
    
    file_idx        = 0
    prev_line_cnt   = -1    

    for the_dir in file_list:
        m = re.search( pattern, the_dir )
        
        if m:
            # Get line count of lines matching pattern
            # Add to line_cnt
            wc = subprocess.check_output( [r'grep -P "Train\ net\ output.*loss\ =\ ([e\-0-9\.]+)\s" ' + the_dir + '/stdout_log | wc'], shell=True)
            m = re.search( "^\s*([e\-0-9\.]+)\s", wc )

            line_cnt = int(m.group(1))

            if prev_line_cnt != -1:
                if line_cnt != prev_line_cnt:
                    print "Error: line_cnt=%d, prev_line_cnt=%d" % (line_cnt, prev_line_cnt)
                    exit( 1 )
            prev_line_cnt = line_cnt
            
            file_idx = file_idx + 1    
#            print "%s: %d" % (the_dir, line_cnt)
    
    the_loss_arr    = np.ndarray(shape=(prev_line_cnt, file_idx), dtype=float, order='C')
    the_dir_arr     = []
    file_idx        = 0
    
    for the_dir in file_list:
        m = re.search( pattern, the_dir )
        
        if m:
            the_dir_arr.append( the_dir )
            fd_src = open( "%s/stdout_log" % the_dir, "r" )
            
            row_idx = 0
            
            while ( 1 ):
                x = fd_src.readline()
                if x == "":
                    break
                
                m = re.search( "Train\ net\ output.*loss\ =\ ([e\-0-9\.]+)\s", x )
                
                if m:
                    the_val = float(m.group(1))
                    the_loss_arr[row_idx][file_idx] = the_val
#                    print "row = %d, col = %d, loss = %f" % (row_idx, file_idx, the_val)
                    row_idx = row_idx + 1
            
            file_idx = file_idx + 1    
            fd_src.close()

    fd_csv = open( csv_filename + ".csv" , "w" )
    for idx in range(file_idx):
        if idx != file_idx - 1:
            fd_csv.write( "%s," % the_dir_arr[idx] )
        else:
            fd_csv.write( "%s\n" % the_dir_arr[idx] )

    it = np.nditer(the_loss_arr, flags=['multi_index'])
    while not it.finished:
        mi = it.multi_index
        if mi[1] == file_idx - 1:
            fd_csv.write( "%f\n" % the_loss_arr[mi] )
        else:
            fd_csv.write( "%f," % the_loss_arr[mi] )
        it.iternext()
    fd_csv.close()

    fd_gpt = open( csv_filename + ".gpt" , "w" )
    fd_gpt.write( r'set datafile separator ","' )
    fd_gpt.write( "\n" )
    for idx in range(file_idx):
        if idx == 0:
            fd_gpt.write( r'  plot "%s.csv" every ::1 using 0:%d with linespoints title "%s"' % (csv_filename, idx+1, the_dir_arr[idx] ) )
        else:
            fd_gpt.write( r'replot "%s.csv" every ::1 using 0:%d with linespoints title "%s"' % (csv_filename, idx+1, the_dir_arr[idx] ) )
        fd_gpt.write( "\n" )

    fd_gpt.write( 'pause -1 "Hit any key to continue"' )
        
#    fd_gpt.write( 'set terminal postscript eps enhanced\n' )
#    fd_gpt.write( 'set output "%s.eps"\n' % csv_filename )
#    fd_gpt.write( 'replot\n' )
    fd_gpt.close()
    