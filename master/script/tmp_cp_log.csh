#!/bin/csh


rm ${COLOMBE_ROOT}/exp/*/stdout* 
rm ${COLOMBE_ROOT}/exp/*/tst* 
rm ${COLOMBE_ROOT}/exp/*/trn* 

foreach myfile ( ${COLOMBE_ROOT}/exp/*/caffe.lp-research-linux-2.mun.log* )

	set my_path = ${myfile:h}

	cp ${myfile} ${my_path}/stdout_log
	echo "Creating...  "${my_path}/stdout_log

end 

echo ""
echo "1) Removed stdout_log file in all directories."
echo "2) Removed trn_accu, trn_loss, tst_accu, tst_loss files."
echo "3) Copied and renamed the original log file to be 'stdout_log'."

