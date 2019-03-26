#!/bin/sh
VER=19.01.1
TGZ=~/rpmbuild/SOURCES/v$VER.tar.gz
#git submodule init
#git submodule update
#for M in dpdk intel-ipsec-mb isa-l ; do
#  (cd $M;
#   git archive \
#        --format=tar.gz --prefix=$M/ -o ~/rpmbuild/SOURCES/spdk-$M-$VER.tar.gz  HEAD
#  )
#done

git archive --format=tar.gz --prefix=spdk-$VER/ -o $TGZ HEAD
