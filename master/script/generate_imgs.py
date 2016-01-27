#!/usr/bin/python

import sys
import os

# Usage: generate_imgs.py <out_root> <n_frames>

if len(sys.argv) != 3:
    print "Usage: %s <out_root> <n_frames>\n\n" % sys.argv[0]
    
else:
    out_root = sys.argv[1]
    n_frames = int(sys.argv[2])
    
    if os.path.exists(out_root + "/jpg"):
        print "The path %s already exists, exiting\n" % (out_root + "/jpg")
        exit()

    system_cmd = "%s/tools/generate_sticks_imgs/generate_sticks_imgs %s 512 512 800 8 200 5 %s HALF" % (os.environ['COLOMBE_ROOT'], n_frames, out_root)
    print "\nsystem_cmd = %s\n" % system_cmd
    os.system( system_cmd )

    # Log the command used to generate the images    
    os.chdir(out_root)
    fd = open( "cmd", mode = 'w')
    fd.write( system_cmd )
    fd.close()
    
    # Create directory for JPEG versions
    os.makedirs("jpg")

    # Convert .bmp to .jpg, while scaling to 256 x 256
    system_cmd = "avconv -i out_%05d.bmp -s 256x256 jpg/out_%05d.jpg"
    print "system_cmd = %s\n" % system_cmd
    os.system( system_cmd )
    
    