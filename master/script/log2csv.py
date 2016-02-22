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
       log2csv.py <pattern> [-l] <csv_filename>
           pattern = regular expression, default is ".*"

       With no arguments all defaults are used.
       Pattern must be defined to use other arguments
       
       Creates files:
         <csv_filename>_test.csv     -- comma separated values (Excel style), Test phase
         <csv_filename>_train.csv    -- comma separated values (Excel style), Train phase
         <csv_filename>.gpt          -- Gnuplot commands, run command:
                                         gnuplot  <csv_filename>.gpt
'''
    exit()
    
# Get the total number of args passed
params_total    = len(sys.argv)

if params_total < 2 or params_total > 4:
    Usage()

else:
    do_loss     = 0
    do_accuracy = 1

    colombe_root = os.environ['COLOMBE_ROOT']
            
    if sys.argv[1] == '-h' or sys.argv[1] == '--help':
        Usage()

    pattern = ".*"
        
    if params_total == 2:
        csv_filename    = sys.argv[1]
    elif params_total == 3:
        pattern         = sys.argv[1]
        if sys.argv[2] != '-l':
            csv_filename    = sys.argv[2]
        else:
            do_loss     = 1
            do_accuracy = 0
    elif sys.argv[2] != '-l':
        Usage()
    else:
        do_loss     = 1
        do_accuracy = 0
        pattern         = sys.argv[1]
        csv_filename    = sys.argv[3]
            
    the_cwd = colombe_root + '/exp'
    os.chdir(the_cwd)
    file_list = os.listdir('.')
    file_list.sort()
    
    file_idx        = 0
    prev_line_cnt   = -1    

    flt_re = r'([e\-0-9\.]+)'
    if do_loss:
        test_flt_str    = "Test net output.*loss = %s " % flt_re
        train_flt_str    = "Train net output.*loss = %s " % flt_re
    else:
        test_flt_str    = "Test.*accuracy = %s" % flt_re
        train_flt_str   = "Train.*accuracy = %s" % flt_re
    
    for the_dir in file_list:
        m = re.search( pattern, the_dir )
        
        if m:
            # Get line count of lines matching pattern
            # Add to line_cnt
            sys_cmd = 'grep -P "%s" %s/stdout_log | wc' % (train_flt_str, the_dir)
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
    
    the_train_arr   = np.ndarray(shape=(prev_line_cnt, file_idx), dtype="i4,f8", order='C')
    the_test_arr    = np.ndarray(shape=(prev_line_cnt, file_idx), dtype="i4,f8", order='C')
    the_dir_arr     = []
    file_idx        = 0
    
    for the_dir in file_list:
        m = re.search( pattern, the_dir )
        
        if m:
            the_dir_arr.append( the_dir )
            fd_src = open( "%s/stdout_log" % the_dir, "r" )
            
            train_row_idx = 0
            test_row_idx  = 0
            
            while ( 1 ):
                x = fd_src.readline()
                if x == "":
                    break
                
                m = re.search( "Iteration ([0-9]+)", x )
                if m:
                    iteration = float(m.group(1))
                m = re.search( train_flt_str, x )
                if m:
                    the_val = float(m.group(1))
                    the_train_arr[train_row_idx][file_idx]['f0'] = iteration
                    the_train_arr[train_row_idx][file_idx]['f1'] = the_val
#                    print "row = %d, col = %d, loss = %f" % (row_idx, file_idx, the_val)
                    train_row_idx = train_row_idx + 1
            
                m = re.search( test_flt_str, x )
                if m:
                    the_val = float(m.group(1))
                    the_test_arr[test_row_idx][file_idx]['f0'] = iteration
                    the_test_arr[test_row_idx][file_idx]['f1'] = the_val
                    test_row_idx = test_row_idx + 1
#                    print "%d %d\n" % (iteration, test_row_idx)
            
            file_idx = file_idx + 1    
            fd_src.close()

    fd_csv = open( "../plots/" + csv_filename + "_train.csv" , "w" )
    for idx in range(file_idx):
        if idx != file_idx - 1:
            fd_csv.write( "%s," % the_dir_arr[idx] )
        else:
            fd_csv.write( "%s\n" % the_dir_arr[idx] )

    it = np.nditer(the_train_arr, flags=['multi_index'])
    while not it.finished:
        mi = it.multi_index
        if mi[1] == file_idx - 1:
            fd_csv.write( "%f,%i\n" % (the_train_arr[mi]['f1'], the_train_arr[mi]['f0']) )
        else:
            fd_csv.write( "%f," % the_train_arr[mi]['f1'] )
        it.iternext()
    fd_csv.close()
    

    tmp = the_test_arr[0:test_row_idx]
    the_test_arr = tmp
    fd_csv = open( "../plots/" + csv_filename + "_test.csv" , "w" )
    for idx in range(file_idx):
        if idx != file_idx - 1:
            fd_csv.write( "%s," % the_dir_arr[idx] )
        else:
            fd_csv.write( "%s\n" % the_dir_arr[idx] )

    it = np.nditer(the_test_arr, flags=['multi_index'])
    while not it.finished:
        mi = it.multi_index
        if mi[1] == file_idx - 1:
            fd_csv.write( "%f,%i\n" % (the_test_arr[mi]['f1'], the_test_arr[mi]['f0']) )
        else:
            fd_csv.write( "%f," % the_test_arr[mi]['f1'] )
        it.iternext()
    fd_csv.close()
    
    fd_gpt = open( "../plots/" + csv_filename + ".gpt" , "w" )

    fd_gpt.write( 'set key outside\n' )
#    fd_gpt.write( 'set xrange [0:%f]\n' % (iteration * 2) )
    if do_loss:
        fd_gpt.write( 'set title "Loss vs. Training Iteration (Log Scale)" font ",14"\n' )
        fd_gpt.write( 'set logscale y\n' )
    else:
        fd_gpt.write( 'set title "Accuracy vs. Training Iteration" font ",14"\n' )

    fd_gpt.write( r'set datafile separator ","' )
    fd_gpt.write( "\n" )
    for idx in range(file_idx):
        if idx == 0:
            fd_gpt.write( r'  plot "%s/plots/%s_train.csv" every ::1 using %d:%d with points title "%s" lc %d%s' % (colombe_root, csv_filename, file_idx+1, idx+1, the_dir_arr[idx], idx, "\n" ) )
        else:
            fd_gpt.write( r'replot "%s/plots/%s_train.csv" every ::1 using %d:%d with points title "%s" lc %d%s' % (colombe_root, csv_filename, file_idx+1, idx+1, the_dir_arr[idx], idx, "\n" ) )
        fd_gpt.write( r'replot "%s/plots/%s_test.csv" every ::1 using %d:%d with linespoints title "%s_tst" lc %d%s' % (colombe_root, csv_filename, file_idx+1, idx+1, the_dir_arr[idx], idx, "\n" ) )

    fd_gpt.write( 'set terminal postscript noenhanced\n' )
    fd_gpt.write( 'set output "../plots/%s.ps"\n' % csv_filename )
    fd_gpt.write( 'replot\n' )

    fd_gpt.close()
    
    os.system( "gnuplot -persist  %s/plots/%s.gpt" % (colombe_root, csv_filename) )
    