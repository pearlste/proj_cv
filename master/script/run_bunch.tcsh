#!/bin/tcsh

set seed = 7000

while (1)

    set njobs = `ps auxww | grep caffe | grep -v grep | wc -l`

    if (  $njobs < 10 ) then
    
        echo -n "njobs = "
        echo -n $njobs
        echo -n ", seed = "
        echo $seed
        
        set run_cmd = "run_caffe.py -slvcfg_template solver_template.prototxt -slvcfg_defines solver_defines -netcfg_template train_template.prototxt -netcfg_defines train_defines -N SX_RANDOM_SEED=${seed} -N SX_CONV1_NUM_OUT=4 -N SX_CONV2_NUM_OUT=4 -N SX_CONV3_NUM_OUT=4 -N SX_CONV4_NUM_OUT=4 -N SX_CONV5_NUM_OUT=4 -N SX_FC6_NUM_OUT=4 -N SX_FC7_NUM_OUT=16 -N SX_MAX_ITER=8000 c1-4_c2-4_c3-4_c4-4_c5-4_fc6-4_fc7-16_seed${seed}"
        echo $run_cmd
#        echo $run_cmd | batch
        $run_cmd
               
        @ seed = $seed + 1
        
        sleep 1

    endif
    
end
