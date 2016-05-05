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
       log2csv.py <pattern> <csv_filename>

       <pattern> is any regular expression, used for filtering experiments
       
       Creates files:
          $COLOMBE_ROOT/plots/<csv_filename>_loss.gpt          
          $COLOMBE_ROOT/plots/<csv_filename>_accuracy.gpt          
          
       To run gnuplot command files, run, e.g.:

            gnuplot -persist $COLOMBE_ROOT/plots/<csv_filename>_loss.gpt
'''
    exit()
    
# Get the total number of args passed
params_total    = len(sys.argv)

if params_total != 3:
    Usage()

else:
    pattern         = sys.argv[1]
    csv_filename    = sys.argv[2]
            
    colombe_root = os.environ['COLOMBE_ROOT']
    the_cwd = colombe_root + '/exp'
    os.chdir(the_cwd)

    fd_loss_gpt = open( "../plots/" + csv_filename + "_loss.gpt" , "w" )
    fd_loss_gpt.write( 'unset key\n' )
    fd_loss_gpt.write( 'set title "Loss vs. Training Iteration (Log Scale)" font ",14"\n' )
    fd_loss_gpt.write( 'set logscale y\n' )
    fd_loss_gpt.write( r'set datafile separator " "' )
    fd_loss_gpt.write( "\n" )

    fd_accu_gpt = open( "../plots/" + csv_filename + "_accuracy.gpt" , "w" )
    fd_accu_gpt.write( 'unset key\n' )
    fd_accu_gpt.write( 'set title "Accuracy vs. Training Iteration" font ",14"\n' )
    fd_accu_gpt.write( r'set datafile separator " "' )
    fd_accu_gpt.write( "\n" )

    file_list = os.listdir('.')
    file_list.sort()

    idx = 0    
    for the_dir in file_list:
        m = re.search( pattern, the_dir )
        if m:
            # Check for existence of stats files
            dir_exists = 1
            try:
                loss_file = "tst_loss"
                fd = open( "%s/%s" % (the_dir, loss_file), "r" )
                fd.close();
                loss_file = "tst_accu"
                fd = open( "%s/%s" % (the_dir, loss_file), "r" )
                fd.close();
                loss_file = "trn_loss"
                fd = open( "%s/%s" % (the_dir, loss_file), "r" )
                fd.close();
                loss_file = "trn_accu"
                fd = open( "%s/%s" % (the_dir, loss_file), "r" )
                fd.close();
                
            except (OSError, IOError) as e:
                dir_exists = 0
                print "Note: stats file %s/%s does not exist ..." % (the_dir, loss_file)
                continue
            
            if idx == 0:
                fd_loss_gpt.write( '  plot "%s/exp/%s/tst_loss" using 1:2 with lines title "%s_tst" lc %d\n' % (colombe_root, the_dir, the_dir, idx) )
                fd_accu_gpt.write( '  plot "%s/exp/%s/tst_accu" using 1:2 with lines title "%s_tst" lc %d\n' % (colombe_root, the_dir, the_dir, idx) )
            else:
                fd_loss_gpt.write( 'replot "%s/exp/%s/tst_loss" using 1:2 with lines title "%s_tst" lc %d\n' % (colombe_root, the_dir, the_dir, idx) )
                fd_accu_gpt.write( 'replot "%s/exp/%s/tst_accu" using 1:2 with lines title "%s_tst" lc %d\n' % (colombe_root, the_dir, the_dir, idx) )

            idx += 1

    fd_loss_gpt.write( 'set terminal postscript noenhanced\n' )
    fd_loss_gpt.write( 'set output "../plots/%s_loss.ps"\n' % csv_filename )
    fd_loss_gpt.write( 'replot\n' )
    fd_loss_gpt.close()
    
    fd_accu_gpt.write( 'set terminal postscript noenhanced\n' )
    fd_accu_gpt.write( 'set output "../plots/%s_accuracy.ps"\n' % csv_filename )
    fd_accu_gpt.write( 'replot\n' )
    fd_accu_gpt.close()
    
    os.system( "gnuplot -persist  %s/plots/%s_accuracy.gpt" % (colombe_root, csv_filename) )
    os.system( "gnuplot -persist  %s/plots/%s_loss.gpt" % (colombe_root, csv_filename) )
    