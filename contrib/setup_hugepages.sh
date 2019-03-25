#!/bin/bash -e
# libhugetlbfs-utils
hugeadm --create-mounts
fn=/sys/kernel/mm/hugepages/hugepages-524288kB/nr_hugepages
if [ -e "$fn" ] ; then
  n=$(cat $fn)
  if [ "$n" -eq 0 ] ; then
    echo 6 > $fn
  fi
fi
fn=/sys/kernel/mm/hugepages/hugepages-1048576kB/nr_hugepages
if [ -e "$fn" ] ; then
  n=$(cat $fn)
  if [ "$n" -eq 0 ] ; then
    echo 3 > $fn
  fi
fi
fn=/sys/kernel/mm/hugepages/hugepages-2048kB/nr_hugepages
if [ -e "$fn" ] ; then
  n=$(cat $fn)
  if [ "$n" -lt 1024 ] ; then
    echo 1024 > $fn
  fi
fi
exit 0
