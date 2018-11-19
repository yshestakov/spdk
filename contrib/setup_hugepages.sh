#!/bin/bash -e
fn=/sys/kernel/mm/hugepages/hugepages-524288kB/nr_hugepages
if [ -e "$fn" ] ; then
  n=$(cat $fn)
  if [ "$n" -eq 0 ] ; then
    echo 16 > $fn
  fi
fi
fn=/sys/kernel/mm/hugepages/hugepages-2048kB/nr_hugepages
if [ -e "$fn" ] ; then
  n=$(cat $fn)
  if [ "$n" -lt 100 ] ; then
    echo 256 > $fn
  fi
fi
exit 0
