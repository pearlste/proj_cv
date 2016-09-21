#!/usr/bin/python

# Usage: gen_caffe_lmdb_scr.py <jpg_path> <start_idx> <n_frames>

import sys
import os
import re

if len(sys.argv) != 4:
    print "\nUsage: %s <jpg_path> <start_idx> <n_frames>" % sys.argv[0]
    print "       n_frames refers to the number of images of *EACH* class"
    print "       Set n_frames=-1 to take all frames\n"
    exit()

else:
   
    the_files = []
     
    jpg_path = sys.argv[1]
    start_idx = int(sys.argv[2])
    n_frames = int(sys.argv[3])
    
    if not os.path.exists(jpg_path):
        print "The JPEG directory %s does not exist, exiting\n" % jpg_path
        exit()

    file_list = os.listdir(jpg_path)
    
    for the_file in file_list:
        m = re.search( "[a-zA-Z\.\-_]*([0-9]+).jpg", the_file )
        
        if m:
            file_num = m.group( 1 )
            the_files = the_files + [the_file]

    the_files.sort()

    num_files = len(the_files)
    
    if n_frames == -1:
        # Take all frames
        n_frames = num_files / 2 

    for i in range(n_frames):
        print "%s/%s 1" % (jpg_path, the_files[start_idx + i]) 

    for i in range(n_frames):
        print "%s/%s 0" % (jpg_path, the_files[start_idx + i + num_files/2]) 
    
