#!/usr/local/bin/python

# Usage: run_caffe.py -slvcfg_template <sct_filename> -slvcfg_defines <scd_filename>
#                     -netcfg_template <nct_filename> -netcfg_defines <ncd_filename>
#                     -N param1=numerical1 -N param2=numerical2 ...
#                     -S paramN=stringN    -S paramNplus1=stringNplus1 <exppath>

# (1) mkdir -p <exppath>
# (2) mkdir -p <exppath>/snaps
# (3) Change the working directory to <exppath>

# (4) In the <exppath> directory create a file 'define_orerrides' with lines like:
#       #define param1              val1
#       #define param2              val2
#            ...                    
#       #define paramN              valN

# (5) Run:
#       cat ${PROJ_ROOT}/cfg/<scd_filename> define_overrides ${PROJ_ROOT}/cfg/<sct_filename> | cpp -P >
#           solver.prototxt

# (6) Run:
#       cat ${PROJ_ROOT}/cfg/<ncd_filename> define_overrides ${PROJ_ROOT}/cfg/<nct_filename> | cpp -P >
#           train_val.prototxt

# Run:
#   $CAFFE_ROOT/build/tools/caffe train --solver=solver.prototxt

import sys
import itertools
import os

def Usage():
    print '''
Usage: run_caffe.py -slvcfg_template <sct_filename> -slvcfg_defines <scd_filename>
                -netcfg_template <nct_filename> -netcfg_defines <ncd_filename>
                -N param1=numerical1 -N param2=numerical2 ...
                -S paramN=stringN    -S paramNplus1=stringNplus1 <exppath>
                '''
    exit()
    
# Includes command name, <exppath> and and required cfg options and names
NUM_REQD_PARAMS = 10
 
# Get the total number of args passed to the demo.py
params_total    = len(sys.argv)

params_optional = params_total - NUM_REQD_PARAMS

if (params_optional % 2) != 0 or params_optional < 0:
    print '%d optional params\n' % params_optional
    Usage()
    
sct_filename = ""
scd_filename = ""
nct_filename = ""
ncd_filename = ""

defines_numer_list = [];
defines_strng_list = [];

# For now ignore the command name, which is the first argument, and the <exppath> which is the last
variable_args = sys.argv[1:(params_total - 1)];

the_iterator = variable_args.__iter__()    
for argidx in the_iterator :
    if argidx[0] != '-':
        print "Error: found %s, was expecting option starting with '-'\n" % argidx
        exit()
    if argidx == '-slvcfg_template':
        sct_filename = next(the_iterator)
    elif argidx == '-slvcfg_defines':
        scd_filename = next(the_iterator)
    elif argidx == '-netcfg_template':
        nct_filename = next(the_iterator)
    elif argidx == '-netcfg_defines':
        ncd_filename = next(the_iterator)
    elif argidx == '-N':
        the_define = next(the_iterator)
        defines_numer_list.append(the_define)
        print 'define: ' + the_define
    elif argidx == '-S':
        the_define = next(the_iterator)
        defines_strng_list.append(the_define)
        print 'define: ' + the_define
    else:
        print "Bad option %s" % argidx

print        
if sct_filename == "":
    print "Error: must define option %s\n\n" % "-slvcfg_template"
    Usage()
elif scd_filename == "":
    print "Error: must define option %s\n\n" % "-slvcfg_defines" 
    Usage()
elif nct_filename == "":
    print "Error: must define option %s\n\n" % "-netcfg_template"
    Usage()
elif ncd_filename == "":
    print "Error: must define option %s\n\n" % "-netcfg_defines" 
    Usage()
else:
    print "sct_filename = %s" % sct_filename
    print "scd_filename = %s" % scd_filename
    print "nct_filename = %s" % nct_filename
    print "ncd_filename = %s" % ncd_filename
    print
    
    exppath = os.environ['COLOMBE_ROOT'] + "/exp/" + sys.argv[-1]
    cfgpath = os.environ['COLOMBE_ROOT'] + "/cfg"
    
    print exppath
    print
    
    if os.path.exists(exppath):
        print "The path %s already exists, exiting\n" % exppath
        exit()

    os.makedirs(exppath)                # Step (1)
    os.makedirs(exppath+"/snaps")       # Step (2)
    os.chdir(exppath)                   # Step (3)

    fd = open( "scr_cmd", mode = 'w')
    for the_str in sys.argv:
        fd.write( "%s " % the_str )
    fd.close()
    
# (4) In the <exppath> directory create a file 'define_orerrides' with lines like:
#       #define param1              val1
#       #define param2              val2
#            ...                    
#       #define paramN              valN

    fd = open( "define_overrides", mode = 'w')
    
    for the_define in defines_numer_list:
        the_line = the_define.split( "=", 1 )
        fd.write( "#undef %s\n" % the_line[0] )
        fd.write( "#define %s %s\n" % (the_line[0], the_line[1]) )

    for the_define in defines_strng_list:
        the_line = the_define.split( "=", 1 )
        fd.write( "#undef %s\n" % the_line[0] )
        fd.write( '#define %s "%s"\n' % (the_line[0], the_line[1]) )

    # Add the lines that will be used to configure the solver.prototxt file
    fd.write( '#define SX_TRAIN_VAL_FILENAME_WITH_PATH "%s/train_val.prototxt"\n' % exppath )
    fd.write( '#define SX_SNAPSHOT_PREFIX              "%s/snaps/snap_"\n' % exppath )

    fd.close()
    
# (5) Run:
#       cat ${PROJ_ROOT}/cfg/<scd_filename> define_overrides ${PROJ_ROOT}/cfg/<sct_filename> | cpp -P >
#           solver.prototxt

    system_cmd = 'cat %s/cfg/%s define_overrides %s/cfg/%s | cpp -P -o solver.prototxt' % \
    (os.environ['COLOMBE_ROOT'], scd_filename, os.environ['COLOMBE_ROOT'], sct_filename)
    print "system_cmd = %s\n" % system_cmd
    os.system( system_cmd )

# (6) Run:
#       cat ${PROJ_ROOT}/cfg/<ncd_filename> define_overrides ${PROJ_ROOT}/cfg/<nct_filename> | cpp -P >
#           train_val.prototxt

    system_cmd = 'cat %s/%s define_overrides %s/%s | cpp -P -o train_val.prototxt' % \
    (cfgpath, ncd_filename, cfgpath, nct_filename)
    print "system_cmd = %s\n" % system_cmd
    os.system( system_cmd )

# (7) Ensure that the following lines are in the the file <sct_filename>:
#       net:                SX_TRAIN_VAL_FILENAME_WITH_PATH
#       snapshot_prefix:    SX_SNAPSHOT_PREFIX

    system_cmd = '$CAFFE_ROOT/build/tools/caffe train -log_dir %s --solver=%s/solver.prototxt >& stdout_log &' % (exppath, exppath)
    print "system_cmd = %s\n" % system_cmd
    
    fd = open( "cmd", mode = 'w')
    fd.write( system_cmd )
    fd.close()
    
    os.system( system_cmd )
    