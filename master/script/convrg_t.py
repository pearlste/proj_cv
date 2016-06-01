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

            break

    # At this point num_bins still represents the maximum number of iterations,
    # not yet scaled by iteration_delta
    best_conv_time  = num_bins

    num_bins /= iteration_delta
    print "Note: iteration_delta=%3d, num_bins=%3d\n" % (iteration_delta, num_bins)            

    best_exp        = ""
    the_histo       = np.zeros(num_bins)
    convrg_t_arr    = []
    files_processed = 0
    
    for the_dir in file_list:
        m = re.search( pattern, the_dir )
        
        if m:
            fd_src = open( "%s/tst_accu" % the_dir, "r" )
            
            rise_start = 0
            
            while ( 1 ):
                x = fd_src.readline()
                if x == "":
                    # We reached EOF without ever surpassing acc_thr1
                    the_histo[num_bins-1] += 1
                    # print "%40s: never" % the_dir
                    break
                
                m = re.search( "([0-9\.]+)\s+([0-9\.]+)", x )
                if m:
                    iteration   = int(m.group(1))
                    the_val     = float(m.group(2))
                    
                    if the_val >= acc_thr2:
                        if rise_start == 0:
                            # Crossing both thresholds on the same iteration, no time difference between them
                            rise_start = iteration

                        conv_time = iteration-rise_start
                        if conv_time < best_conv_time:
                            best_conv_time  = conv_time
                            best_exp        = the_dir
                        
                        convrg_t_arr = np.append(convrg_t_arr, [conv_time])
                        # Previously surpassed acc_thr1 at rise-start, add up-tick to histogram based on
                        # iteration - rise_start
                        the_histo[conv_time/iteration_delta] += 1
 
                        # Once we've surpassed acc_thr2, nothing more to look at, so break
                        # print "%40s: %7d" % (the_dir, iteration-rise_start)
                        break
 
                    elif rise_start == 0 and the_val >= acc_thr1:
                        rise_start = iteration
                    
            fd_src.close()
            files_processed += 1
                    
    print "Out of %d experiments, best: %s, time=%d\n" % (files_processed, best_exp, best_conv_time)

    proj_root  = os.environ['COLOMBE_ROOT']
    print "Saving files:"
    print '   %s/plots/%s_%s_%1.2f_%1.2f.mat' % (proj_root, outfile, 'convrg_t_raw', acc_thr1, acc_thr2)
    print '   %s/plots/%s_%s_%1.2f_%1.2f.mat' % (proj_root, outfile, 'convrg_t_hst', acc_thr1, acc_thr2)
    print ''
    
    scipy.io.savemat('%s/plots/%s_%s_%1.2f_%1.2f.mat' % (proj_root, outfile, 'convrg_t_raw', acc_thr1, acc_thr2), mdict={'convrg_t_raw_0_%2d__0_%2d' % (int(round(acc_thr1*100)), int(round(acc_thr2*100))): convrg_t_arr})
    scipy.io.savemat('%s/plots/%s_%s_%1.2f_%1.2f.mat' % (proj_root, outfile, 'convrg_t_hst', acc_thr1, acc_thr2), mdict={'convrg_t_hst_0_%2d__0_%2d' % (int(round(acc_thr1*100)), int(round(acc_thr2*100))): the_histo})
    
#    plt.plot(the_histo[0:num_bins-2])
#    pylab.show()
