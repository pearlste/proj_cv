#!/usr/local/bin/python

import sys

#sys.path.insert(0, '/usr/local/lib/python2.7/site-packages')
#sys.path.insert(0, '/usr/local/lib/python2.7/site-packages/google/protobuf')
#sys.path.insert(0, '/usr/local/lib/python2.7/site-packages/matplotlib')

import numpy as np
import scipy.io
import matplotlib.pyplot as plt
import os
import pylab

def Usage():
    print '''
Usage: dump_weights.py <expdir>

  The results will be stored in a bunch of (e.g. 9) .mat files
  in the 'plots' subdirectory.
  
  Use the MATLAB function 'plot_conv' to take these files, and
  create an animated GIF, that can be viewed with 'imagej'.
  
                '''
    exit()
    
if (len(sys.argv) != 2):
    Usage()
    
caffe_root = os.environ['CAFFE_ROOT']
proj_root  = os.environ['COLOMBE_ROOT']

exp = sys.argv[1]
exppath = proj_root + "/exp/" + exp
os.chdir(exppath)

sys.path.insert(0, caffe_root + '/python')

print sys.path

import caffe

plt.rcParams['figure.figsize'] = (10, 10)
plt.rcParams['image.interpolation'] = 'nearest'
plt.rcParams['image.cmap'] = 'gray'

caffe.set_mode_cpu()

NUM_TESTS       = 100
ITERS_PER_TEST  = 80
TOTAL_ITERS     = NUM_TESTS * ITERS_PER_TEST


for i in range(0, 8):
    # the parameters are a list of [weights, biases]
    layer_num = i+1
    if layer_num < 6:
        layer_str = 'conv%d' % layer_num
    else:
        layer_str = 'fc%d' % layer_num
            
    print layer_str
    
    for iteration in range (0, TOTAL_ITERS, ITERS_PER_TEST):
        
        the_iter = iteration + ITERS_PER_TEST
        the_idx  = iteration / ITERS_PER_TEST;
        
        net = caffe.Net(proj_root + '/exp/' + exp + '/train_val.prototxt',
                        proj_root + '/exp/' + exp + '/snaps/snap__iter_%d.caffemodel'%the_iter,
                        caffe.TEST)
        
        # input preprocessing: 'data' is the name of the input blob == net.inputs[0]
    #    transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})
    #    transformer.set_raw_scale('data', 255)  # the reference model operates on images in [0,255] range instead of [0,1]
    #    
    #    [(k, v.data.shape) for k, v in net.blobs.items()]
    #    
    #    [(k, v[0].data.shape) for k, v in net.params.items()]
        
        filters = net.params[layer_str][0].data
        
        # print "Layer %s:  pre-squeeze filters.shape=%s" % (layer_str, str(filters.shape))
        
        filters = filters.squeeze()
    
        if the_idx == 0:
            all_filters = np.zeros( (NUM_TESTS, ) + filters.shape)
        
        all_filters[the_idx, :] = filters
            
        # print "Layer %s: post-squeeze filters.shape=%s" % (layer_str, str(filters.shape))
        
        #print str(filters)
        
        del filters
        del net
            
    scipy.io.savemat('%s/plots/%s_%s.mat' % (proj_root, exp, layer_str), mdict={'weights': all_filters})

    del all_filters
    