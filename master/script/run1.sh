 run_caffe.py                                                                                                    \
 -slvcfg_template solver_template.prototxt                                                                      \
 -slvcfg_defines solver_defines                                                                                 \
 -netcfg_template train_template.prototxt                                                                       \
 -netcfg_defines train_defines                                                                                  \
 -S SX_DATA_TRAIN_MEAN_FILENAME="/home/pearlstl/proj_cv/master/lmdb/synth1_train_lum_db/mean_file.binaryproto"  \
 -S SX_DATA_TRAIN_LMDB_NAME="/home/pearlstl/proj_cv/master/lmdb/synth1_train_lum_db"                            \
 -S SX_DATA_TEST_MEAN_FILENAME="/home/pearlstl/proj_cv/master/lmdb/synth1_test_lum_db/mean_file.binaryproto"    \
 -S SX_DATA_TEST_LMDB_NAME="/home/pearlstl/proj_cv/master/lmdb/synth1_test_lum_db"                              \
 -N SX_RANDOM_SEED=0                                                                                            \
 -N SX_TEST_ITER=10                                                                                             \
 -N SX_TEST_INTERVAL=100                                                                                        \
 -N SX_BASE_LR=0.001                                                                                            \
 -N SX_STEPSIZE=100000                                                                                          \
 -N SX_DISPLAY=10                                                                                               \
 -N SX_MAX_ITER=1600                                                                                            \
 -N SX_MOMENTUM=0.9                                                                                             \
 -N SX_WEIGHT_DECAY=0.0005                                                                                      \
 -N SX_SHAPSHOT=100 gray_8000                                                                                   
 