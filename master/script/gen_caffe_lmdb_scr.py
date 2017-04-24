#!/usr/bin/python

# Usage: gen_caffe_lmdb_scr.py <jpg_path> <start_idx> <n_frames>

import sys
import os
import re

if len(sys.argv) < 4:
    print "Option 1: \nUsage: %s <jpg_path> <start_idx> <n_frames>" % sys.argv[0]
    print "	Example) %s gen_caffe_lmdb_scr.py /home/../imgs 0 -1 > /dir/label_file.txt" % sys.argv[0]
    print ""
    print "Option 2: \nUsage: %s <jpg_path1> <class #> <jpg_path2> <class #> <jpg_path3> <class #>" % sys.argv[0]
    print "	Example) %s gen_caffe_lmdb_scr.py /home/../imgs0 0 /home/../imgs1 1 /home/../imgs2 2 > /dir/label_file.txt" % sys.argv[0]
    print "		 This example will put the list of labels into the text file."
    print ""
    print ""
    print "Note:"
    print "       n_frames refers to the number of images of *EACH* class"
    print "       Set n_frames=-1 to take all frames\n"
    exit()

elif len(sys.argv) == 4:

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





elif len(sys.argv) > 4:
   
    even_argvs = []
    odd_argvs = []
    for i in range(len(sys.argv)):
	if (i % 2) == 0 and i != 0:
	    even_argvs.append(sys.argv[i])
	elif (i % 2) != 0 :
	    odd_argvs.append(sys.argv[i])
  
    num_class = len(even_argvs)

    file_list = []
    num_files = []
    for i in range(len(odd_argvs)):
	
	#num_files = len([f for f in os.listdir(even_argvs[i]) if os.path.isfile(os.path.join(path, f))])

    	if not os.path.exists(odd_argvs[i]):
            print "The JPEG directory %s does not exist, exiting\n" % odd_argvs[i]
            exit()

    	file_list.append(os.listdir(odd_argvs[i]))
	num_files.append(len(file_list[i]))
	#print(file_list)
	#print(num_files)
        
	the_files = []
        for the_file in file_list[i]:
            m = re.search( "[a-zA-Z\.\-_]*([0-9]+).jpg", the_file )
       
            if m:
                file_num = m.group( 1 )
                the_files = the_files + [the_file]

    		the_files.sort()

   		#num_files = len(the_files)
    
        for j in range(num_files[i]):
            print "%s/%s %s" % (odd_argvs[i], the_files[j], i) 
    
