#!/bin/bash
# --user $UID \
# centos75-spdk -> centos75-mofed46
docker run  \
    --name build-spdk01 \
    -e "VER=19.04" -e "BUILD_NUMBER=2" \
    -v ~/rpmbuild:/rpmbuild \
    -v `pwd`:/scratch         \
    --rm -i         \
    -t harbor.mellanox.com/swx-storage/`uname -m`/centos75-mofed46 \
    /scratch/scripts/build_rpm.sh
