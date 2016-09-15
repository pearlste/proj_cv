#!/usr/local/bin/python

# This script examines all of the experiments, determines the root part of each
# and reports all of the unique experiment names, and how many of each

import sys
import os
import re
import subprocess

#Read in all subdirs in exp directory, keep track of unique names

colombe_root = os.environ['COLOMBE_ROOT']
the_cwd = colombe_root + '/exp'
os.chdir(the_cwd)

file_list = os.listdir('.')
file_list.sort()

prev_dir = ""

num_exps = 0

for the_dir in file_list:
    # get rid of everything after _seed
    m = re.search( "(.*)_seed.*", the_dir );

    if m:
        cur_dir = m.group(1)
        
        if cur_dir != prev_dir:
#            print "%s:%s" % (cur_dir, prev_dir)

            print "%5d exps\n%48s: " % (num_exps, cur_dir),
            prev_dir = cur_dir
            num_exps = 1
        else:
            num_exps += 1

print "%5d exps\n" % (num_exps)

