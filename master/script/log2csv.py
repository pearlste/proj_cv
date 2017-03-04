#!/usr/local/bin/python

import sys
import os
import re
import subprocess
import numpy as np
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-s',       action='store_true', help='single experiment mode')
parser.add_argument('-k',       action='store_true', help='add plot legend'       )
parser.add_argument('-tstl',    action='store_true', help='include test loss'     )
parser.add_argument('-tsta',    action='store_true', help='include test accuracy' )
parser.add_argument('-trnl',    action='store_true', help='include train loss'    )
parser.add_argument('-trna',    action='store_true', help='include train accuracy')
parser.add_argument('pattern',     help='regular expression specifying set of experiments in $COLOMBE_ROOT/exp' )
parser.add_argument('csv_filename_root', default='pf', nargs='?', help='filename root for gnuplot scripts written to $COLOMBE_ROOT/plots/*.gpt')
args = parser.parse_args()

# Usage: log2csv.py -s -tstl -tsta -trnl -trna <pattern> <csv_filename_root>

mode_sing = 0
mode_lgnd = 0
mode_tstl = 0
mode_tsta = 1
mode_trnl = 0
mode_trna = 0

if args.s:
    mode_sing = 1
if args.k:
    mode_lgnd = 1
if args.tstl:
    mode_tstl = 1
if args.tsta:
    mode_tsta = 1
if args.trnl:
    mode_trnl = 1
if args.trna:
    mode_trna = 1

pattern         = args.pattern
csv_filename    = args.csv_filename_root
        
colombe_root = os.environ['COLOMBE_ROOT']
the_cwd = colombe_root + '/exp'
os.chdir(the_cwd)

fd_dict = { }

for tst_trn in ( 'tst', 'trn' ):
    for loss_accu in ( 'loss', 'accu' ):

        type_str = tst_trn + "_" + loss_accu
        
        if (tst_trn == 'tst' and loss_accu == 'loss' and mode_tstl) or \
           (tst_trn == 'tst' and loss_accu == 'accu' and mode_tsta) or \
           (tst_trn == 'trn' and loss_accu == 'loss' and mode_trnl) or \
           (tst_trn == 'trn' and loss_accu == 'accu' and mode_trna):
            
            if loss_accu == 'loss':
                y_title = 'set title "Loss vs. Training Iteration (Log Scale)" font ",14"\n'
            else:
                y_title = 'set title "Accuracy vs. Training Iteration" font ",14"\n'
                
            fd_dict[type_str] = open( "../plots/" + csv_filename + "_" + type_str + ".gpt" , "w" )
            if not mode_lgnd:
                fd_dict[type_str].write( 'unset key\n' )
            fd_dict[type_str].write(y_title)
            if loss_accu == 'loss':
                fd_dict[type_str].write( 'set logscale y\n' )
            fd_dict[type_str].write( r'set datafile separator " "' )
            fd_dict[type_str].write( "\n" )
        else:
            fd_dict[type_str] = None

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
            plot_cmd = '  plot'
        else:
            plot_cmd = 'replot'
        
        for tst_trn in ( 'tst', 'trn' ):
            for loss_accu in ( 'loss', 'accu' ):
        
                type_str = tst_trn + "_" + loss_accu
                #print( type_str, fd_dict[type_str] )
                if fd_dict[type_str] is not None:
                    fd_dict[type_str].write( '%s "%s/exp/%s/%s" using 1:2 with lines title "%s_%s" lc %d\n' % (plot_cmd, colombe_root, the_dir, type_str, the_dir, type_str, idx) )

        idx += 1

for tst_trn in ( 'tst', 'trn' ):
    for loss_accu in ( 'loss', 'accu' ):

        type_str = tst_trn + "_" + loss_accu
        if fd_dict[type_str] is not None:
            fd_dict[type_str].write( 'set terminal postscript noenhanced\n' )
            fd_dict[type_str].write( 'set output "%s/plots/%s_%s.ps"\n' % (colombe_root, csv_filename, type_str) )
            fd_dict[type_str].write( 'replot\n' )
            fd_dict[type_str].close()
            
            os.system( "gnuplot -persist  %s" % fd_dict[type_str].name )

