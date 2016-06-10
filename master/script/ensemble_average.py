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
Usage: ensemble_average.py -h
       ensemble_average.py --help
       ensemble_average.py <pattern> <outfile>

           pattern  = regular expression, default is ".*"

'''
    exit()
    
# Get the total number of args passed
params_total    = len(sys.argv)

if params_total != 3:
    Usage()

else:
    colombe_root = os.environ['COLOMBE_ROOT']
            
    if sys.argv[1] == '-h' or sys.argv[1] == '--help':
        Usage()

    pattern         = sys.argv[1]
    outfile         = sys.argv[2]
        
    the_cwd = colombe_root + '/exp'
    os.chdir(the_cwd)
    file_list = os.listdir('.')
    file_list.sort()
    
    # Find iteration_delta based on the iteration listed for the 2nd entry
    #   ... check to see that it is constant among all stats files examined
    # Find num_bins based on the maximum iteration seen among all files
    
    iteration_delta = 0
    num_bins        = 0
    
    files_processed = 0
    
    print ""
    
    for the_dir in file_list:
        m = re.search( pattern, the_dir )
        
        if m:
            # Get line 2            
            sys_cmd = 'head -2 %s/tst_accu | tail -1' % the_dir
            the_line = subprocess.check_output( [sys_cmd], shell=True)
            m = re.search( "([0-9\.]+)\s+([0-9\.]+)", the_line )
            new_iteration_delta = int(m.group(1))
            
            if iteration_delta != 0 and iteration_delta != new_iteration_delta:
                print "Error: file %s/tst_accu, iteration_delta=%d, new_iteration_delta=%d" % (the_dir, iteration_delta, new_iteration_delta)
                exit()
            else:
                iteration_delta = new_iteration_delta
                
            # Get last line
            sys_cmd = 'tail -1 %s/tst_accu' % the_dir
            the_line = subprocess.check_output( [sys_cmd], shell=True)
            m = re.search( "([0-9\.]+)\s+([0-9\.]+)", the_line )
            new_num_bins = int(m.group(1))
            
            if new_num_bins > num_bins:
                num_bins = new_num_bins
                print "Note: %s/tst_accu, new_num_bins=%3d\n" % (the_dir, new_num_bins)
            
            files_processed += 1
            if (files_processed % 1000) == 0:
                sys.stdout.write("%5d ...\n" % files_processed)
                sys.stdout.flush()

            # Get number of lines
            sys_cmd = 'wc -l %s/tst_accu' % the_dir
            the_line = subprocess.check_output( [sys_cmd], shell=True)
            m = re.search( "([0-9\.]+)\s", the_line )
            num_vals = int(m.group(1))
            
            break

    # At this point num_bins still represents the maximum number of iterations,
    # not yet scaled by iteration_delta
    num_bins /= iteration_delta
    print "Note: iteration_delta=%3d, num_bins=%3d\n" % (iteration_delta, num_bins)            

    the_accu_avg     = np.zeros(num_vals)
    the_loss_avg     = np.zeros(num_vals)
    
    files_processed = 0
    
    for the_dir in file_list:
        m = re.search( pattern, the_dir )
        
        if m:
            fd_accu = open( "%s/tst_accu" % the_dir, "r" )
            fd_loss = open( "%s/tst_loss" % the_dir, "r" )
                
            for i in range(0, num_vals):
                x = fd_accu.readline()
                if x == "":
                    # We reached EOF without ever surpassing acc_thr1
                    print "Reached EOF at line %d in file %s\n" % (i, "%s/tst_accu" % the_dir)
                    exit()
                
                m = re.search( "([0-9\.]+)\s+([0-9\.]+)", x )
                if m:
                    iteration   = int(m.group(1))
                    the_val     = float(m.group(2))
                    the_accu_avg[i] += the_val
                    
                x = fd_loss.readline()
                if x == "":
                    # We reached EOF without ever surpassing acc_thr1
                    print "Reached EOF at line %d in file %s\n" % (i, "%s/tst_loss" % the_dir)
                    exit()
                
                m = re.search( "([0-9\.]+)\s+([0-9\.]+)", x )
                if m:
                    iteration   = int(m.group(1))
                    the_val     = float(m.group(2))
                    the_loss_avg[i] += the_val
                    
            fd_accu.close()
            fd_loss.close()
            files_processed += 1
                    
    proj_root  = os.environ['COLOMBE_ROOT']
    print "Saving files:"
    print '   %s/plots/%s_%s.mat' % (proj_root, outfile, 'ensemble_accu')
    print '   %s/plots/%s_%s.mat' % (proj_root, outfile, 'ensemble_loss')
    print ''
    
    scipy.io.savemat('%s/plots/%s_%s.mat' % (proj_root, outfile, 'ensemble_accu'), mdict={'ensemble_accu_%s' % outfile: the_accu_avg})
    scipy.io.savemat('%s/plots/%s_%s.mat' % (proj_root, outfile, 'ensemble_loss'), mdict={'ensemble_loss_%s' % outfile: the_loss_avg})
    
#    plt.plot(the_histo[0:num_bins-2])
#    pylab.show()
