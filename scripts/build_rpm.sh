#!/bin/bash
args="$@"
wd=$(dirname $0)
wdir=$(dirname $wd)
cd $wdir
mkdir -p $HOME/rpmbuild/{SOURCES,RPMS,SRPMS,SPECS,BUILD,BUILDROOT}
set -e
if [ -z "$VER" ] ; then
    export VER=18.10
fi
branch=$(git rev-parse --abbrev-ref HEAD)
sha1=$(git rev-parse HEAD |cut -c -8)

git archive \
    --format=tar.gz --prefix=spdk-$VER/ -o ~/rpmbuild/SOURCES/spdk-$VER.tar.gz  HEAD
echo ***********
ls -l ~/rpmbuild/SOURCES/spdk-$VER.tar.gz
echo ***********
git submodule init
git submodule update
(cd dpdk;
 git archive \
    --format=tar.gz --prefix=dpdk/ -o ~/rpmbuild/SOURCES/spdk-dpdk-$VER.tar.gz  HEAD
)

(
cd intel-ipsec-mb ;
  git archive \
    --format=tar.gz --prefix=intel-ipsec-mb/ -o ~/rpmbuild/SOURCES/spdk-intel-ipsec-mb-$VER.tar.gz  HEAD
)
# 
set +e
# ./scripts/pkgdep.sh
#yum -q -y install \
#  kernel-devel doxygen graphviz python-configshell 
set -e

# BUILD_NUMBER is an env var passed by Jenkins
# https://stackoverflow.com/questions/16155792/using-jenkins-build-number-in-rpm-spec-file
fakeroot  \
  rpmbuild -bs \
    -D "_version ${VER}" -D "_rev ${BUILD_NUMBER:-1}" \
    --define "_branch ${branch}" \
    --define "_sha1 ${sha1}" $args \
    scripts/spdk.spec 

rpmbuild -bb \
    -D "_version ${VER}" -D "_rev ${BUILD_NUMBER:-1}" \
    --define "_branch ${branch}" \
    --define "_sha1 ${sha1}" $args \
    scripts/spdk.spec


if [ -d /scratch/upload ] ; then
  cp -p ~/rpmbuild/RPMS/`uname -m`/spdk-*$VER-${BUILD_NUMBER:-1}*.rpm /scratch/upload
  cp -p ~/rpmbuild/SRPMS/spdk-*$VER-${BUILD_NUMBER:-1}*.src.rpm /scratch/upload
fi
