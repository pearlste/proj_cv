#!/bin/tcsh

set seed = 0

while ( $seed < 10 )

    set njobs = `ps auxww | grep caffe | grep -v grep | wc -l`

    if (  $njobs < 30 ) then
    
        echo -n "njobs = "
        echo -n $njobs
        echo -n ", seed = "
        echo $seed
        
        set run_cmd = "run_caffe.py -slvcfg_template solver_template.prototxt_elc470 -slvcfg_defines solver_defines_elc470 -netcfg_template train_template.prototxt_elc470 -netcfg_defines train_defines_elc470 -N SX_RANDOM_SEED=${seed} -N SX_CONV1_NUM_OUT=64 -N SX_CONV2_NUM_OUT=64 -N SX_CONV3_NUM_OUT=64 -N SX_CONV4_NUM_OUT=64 -N SX_CONV5_NUM_OUT=64 -N SX_FC6_NUM_OUT=256 -N SX_FC7_NUM_OUT=256 -N SX_MAX_ITER=8000 elc470__c1-64_c2-64_c3-64_c4-64_c5-64_fc6-256_fc7-256_4c_diff_tstItr_seed${seed}"

        echo $run_cmd
#        echo $run_cmd | batch
        $run_cmd
               
        @ seed = $seed + 1
        
        sleep 10

    endif
    
end
