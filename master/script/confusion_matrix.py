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
Usage: confusion_matrix.py <expdir>
                '''
    exit()
    
if (len(sys.argv) != 2):
    Usage()
    
# Make sure that caffe is on the python path:
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
net = caffe.Net(proj_root + '/exp/' + exp + '/train_val.prototxt',
                proj_root + '/exp/' + exp + '/snaps/snap__iter_1600.caffemodel',
                caffe.TEST)

#im1 = caffe.io.load_image('/home/media/synth/synth1/jpg/out_00001.jpg');
#m1  = im1.mean(0).mean(0);

# input preprocessing: 'data' is the name of the input blob == net.inputs[0]
transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})
#transformer.set_transpose('data', (2,0,1))
#transformer.set_mean('data', m1) # mean pixel
transformer.set_raw_scale('data', 255)  # the reference model operates on images in [0,255] range instead of [0,1]
#transformer.set_channel_swap('data', (2,1,0))  # the reference model has channels in BGR order instead of RGB

# set net to batch size of 50
#net.blobs['data'].reshape(50,3,227,227)

#net.blobs['data'].data[...] = transformer.preprocess('data', im1)
#out = net.forward(blobs=['fc8'])
#print("Predicted class is #{}.".format(out['prob'][0].argmax()))

[(k, v.data.shape) for k, v in net.blobs.items()]

[(k, v[0].data.shape) for k, v in net.params.items()]

# take an array of shape (n, height, width) or (n, height, width, channels)
# and visualize each (height, width) thing in a grid of size approx. sqrt(n) by sqrt(n)
def vis_square(data, padsize=1, padval=0):
    data -= data.min()
    data /= data.max()
    # force the number of filters to be square
    n = int(np.ceil(np.sqrt(data.shape[0])))
    padding = ((0, n ** 2 - data.shape[0]), (0, padsize), (0, padsize)) + ((0, 0),) * (data.ndim - 3)
    data = np.pad(data, padding, mode='constant', constant_values=(padval, padval))
    # tile the filters into an image
    data = data.reshape((n, n) + data.shape[1:]).transpose((0, 2, 1, 3) + tuple(range(4, data.ndim + 1)))
    data = data.reshape((n * data.shape[1], n * data.shape[3]) + data.shape[4:])
    plt.imshow(data)

# the parameters are a list of [weights, biases]
filters = net.params['conv1'][0].data
filters = filters.squeeze()

scipy.io.savemat('%s/plots/plot.mat' % proj_root, mdict={'arr': filters})
    
vis_square(filters.transpose(0, 2, 1))

#feat = net.blobs['conv1'].data[0, :36]
#vis_square(feat, padval=1)
#
#filters = net.params['conv2'][0].data
#vis_square(filters[:48].reshape(64*32, 5, 5))
pylab.show()
    