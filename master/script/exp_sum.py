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
Usage: exp_sum.py -h
       exp_sum.py --help
       exp_sum.py
       exp_sum.py <pattern>

       1) exp_sum.py 
	- summarizes the results of exps with #_of_conv_feats = [4, 8, 16, 32, 64]
	- summarizes into four categories (accu >90%, >95%, >99%, >100%) 

       2) exp_sum.py <exp dir>
	- summarizes the results of exps that starts with <exp dir> 
	
'''
    exit()

# Get the total number of args passed
params_total    = len(sys.argv)

if params_total > 2 or params_total == "exp_sum.py -h" or params_total == "exp_sum.py --help":
    Usage()

else:
    point = 0
    # scores_list_in_pattern = {}
    scores_list_in_pattern = []

    colombe_root = os.environ['COLOMBE_ROOT']
    the_cwd = colombe_root + '/exp'
    os.chdir(the_cwd)
    file_list = os.listdir('.')
    file_list.sort()

    count = 0

    if params_total == 2:
	pattern = sys.argv[1]
	exp_over_90 = 0

   	exp_over_95 = 0

    	exp_over_100 = 0
	
    	for the_dir in file_list:
		if the_dir.startswith("%s" % pattern):
			#print conv_feats
			#print the_dir
			try:
				open_tst_accu = open( "%s/tst_accu" % the_dir, "r" )
			except (OSError, IOError) as e:
				print "\n\n*** Can't open stats file for writing under %s\n\n" % the_dir
				continue
		
			accus = []
			while ( 1 ):
				# Get the next line
				x = open_tst_accu.readline()
					
				if x == "":
					break
			
				tst_accus = x.split(' ')
				accus.append(float(tst_accus[1]))
	
			score = max(accus)
			scores_list_in_pattern.append(score) #keep each best score in the list
	
			#print  '%f is score 1' % score
			
			if score >= 0.9:
				exp_over_90 += 1
			#	print '%f is score inside if.' % score
			#	print '%s is exp_90' % exp_over_90[conv_feats]
			if score >= 0.99:
				exp_over_95 += 1
			if score >= 1.0:
				exp_over_100 += 1

			count += 1

	#print scores_list_in_pattern
    	#print "%d is the number of scores in %s" % (len(scores_list_in_pattern), pattern)
	print "Number of experiments = %s" % count
    	##for conv_feats in files_:
	exp_percentile = (float(exp_over_90*1.00/count), float(exp_over_95*1.00/count), float(exp_over_100*1.00/count))
	#print exp_percentile
	print "Percentage of exps (%s) with accu >= 0.90 is %s" %( pattern, format(exp_percentile[0]*1.00*100, '.4g') )
	print "Percentage of exps (%s) with accu >= 0.99 is %s" %( pattern, format(exp_percentile[1]*1.00*100, '.4g') )
	print "Percentage of exps (%s) with accu =  1.00 is %s " %( pattern, format(exp_percentile[2]*1.00*100, '.4g') )
	print ""
 
	proj_root  = os.environ['COLOMBE_ROOT']
    	print "Saving files:"
    	print '   %s/plots/%s.mat' % (colombe_root, 'exp_summary')
    	print ''
			    
	scipy.io.savemat( '%s/plots/%s.mat' % (colombe_root, 'exp_summary'), mdict = {'exp_percentile_%s_convfeatures' % "hello" : exp_percentile} )


	
    if params_total == 1:
	exp_over_90 = {
		4 : 0, 
		8 : 0, 
		16 : 0, 
		32 : 0, 
		64 : 0
	}

	exp_over_95 = {
		4 : 0, 
		8 : 0, 
		16 : 0, 
		32 : 0, 
		64 : 0
    	}

   	exp_over_100 = {
		4 : 0, 
		8 : 0, 
		16 : 0, 
		32 : 0, 
		64 : 0
    	}	

	conv_feats_set = [4, 8, 16, 32, 64]
	#Now look at the tst_accu to see how many of the exp with same conv_features have converged
    	#Output a number of exps converged to 90%, 95% 99% 100% and save it in one file
    	scores_list_in_eachfeat = {}     

    	for the_dir	in file_list:
		for conv_feats in conv_feats_set:
			scores_list_in_eachfeat.setdefault(conv_feats, [])
			if the_dir.startswith("c1-%s" % conv_feats):
				#print conv_feats
				#print the_dir
				try:
					open_tst_accu = open( "%s/tst_accu" % the_dir, "r" )
				except (OSError, IOError) as e:
					print "\n\n*** Can't open stats file for writing under %s\n\n" % the_dir	
					continue
		
				accus = []
				while ( 1 ):
					# Get the next line
					x = open_tst_accu.readline()
					
					if x == "":
						break
			
					tst_accus = x.split(' ')
					accus.append(float(tst_accus[1]))
	
				score = max(accus)
				scores_list_in_eachfeat[conv_feats].append(score) #keep each best score in the list	
				
	
				#print  '%f is score 1' % score
				
				if score >= 0.9:
					exp_over_90[conv_feats] += 1
				#	print '%f is score inside if.' % score
				#	print '%s is exp_90' % exp_over_90[conv_feats]
				if score >= 0.99:
					exp_over_95[conv_feats] += 1
	
				if score >= 1.0:
					exp_over_100[conv_feats] += 1
		
			#if the_dir.startswith("c1-4"):
				#print the_dir
				#print exp_over_90
				#print '%f is score for %s' % (score, conv_feats)
				#print ""
	
    	#print scores_list_in_eachfeat
	print "Number of experiments #conv_feat=%s is %s" % (4, len(scores_list_in_eachfeat[4]))
	print "Number of experiments #conv_feat=%s is %s" % (8, len(scores_list_in_eachfeat[8]))
	print "Number of experiments #conv_feat=%s is %s" % (16, len(scores_list_in_eachfeat[16]))
	print "Number of experiments #conv_feat=%s is %s" % (32, len(scores_list_in_eachfeat[32]))
	print "Number of experiments #conv_feat=%s is %s" % (64, len(scores_list_in_eachfeat[64]))

    	print ""

	exp_summary = {}
    	for conv_feats in conv_feats_set:
		exp_percentile = [float(exp_over_90[conv_feats]*1.00/len(scores_list_in_eachfeat[conv_feats])), float(exp_over_95[conv_feats]*1.00/len(scores_list_in_eachfeat[conv_feats])), float(exp_over_100[conv_feats]*1.00/len(scores_list_in_eachfeat[conv_feats]))]
		exp_summary.setdefault(conv_feats, [])
		exp_summary[conv_feats].append(exp_percentile)
		
		#print exp_percentile
		print "Percentage of exps (#feat=%s) with accu >= 0.90 is %s" %( conv_feats, format(exp_percentile[0]*1.00*100, '.3g') )
		print "Percentage of exps (#feat=%s) with accu >= 0.99 is %s" %( conv_feats, format(exp_percentile[1]*1.00*100, '.3g') )
		print "Percentage of exps (#feat=%s) with accu =  1.00 is %s" %( conv_feats, format(exp_percentile[2]*1.00*100, '.3g') )
		print ""
	
	print exp_summary
	print ''

    	proj_root  = os.environ['COLOMBE_ROOT']
    	print "Saving files:"
    	print '   %s/plots/%s.mat' % (colombe_root, 'summary_for_all_exp')
    	print ''
	
	scipy.io.savemat( '%s/plots/%s.mat' % (colombe_root, 'exp_summary'), mdict = {'exp_percentile_%s_convfeatures' % "summary_for_all_exp" : exp_summary,} )

