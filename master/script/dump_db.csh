#!/bin/csh

# Usage dump_db <lmdb_name>

set dumpfile = /tmp/lmdb_dump_temp

mdb_dump -p -f $dumpfile ${COLOMBE_ROOT}/lmdb/${1}

lmdump2jpgs.py $dumpfile | more
