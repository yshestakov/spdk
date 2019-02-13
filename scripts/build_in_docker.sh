#!/bin/bash
docker run  \
 --user $UID \
    --name build-spdk01 \
    -e "VER=18.10" -e "BUILD_NUMBER=5" \
    -v ~/rpmbuild:/rpmbuild \
    -v `pwd`:/scratch         \
    --rm -i         \
    -t harbor.mellanox.com/swx-storage/`uname -m`/centos75-spdk \
    /scratch/scripts/build_rpm.sh
