#!/bin/bash

if [ -z "${AS_NUMBER}" ]
then
    >&2 echo "No AS_NUMBER varenv defined. Please define it to be able to build your IPs list."
    exit 1
fi

CURRENT_DIR=`dirname \`readlink -f $0\``

pyasn_util_download.py --latest
pyasn_util_convert.py --single rib.*.bz2 ipasn.dat

# the content of ipasn.dat will be something like:
# 127.0.0.1/24 12345
# 128.0.0.1/25 65432

# `65432` or `65432` being an AS number and the IP range before it being a subnet owned by the AS

# Next line finds every IP ranges owned by $AS_NUMBER in `ipasn.dat` and outputs it in `ips.list`
grep -oP "\K([/.\d]+)(?=\s+${AS_NUMBER})" ipasn.dat | sort | uniq > ${CURRENT_DIR}/ips.list

rm rib.*.bz2 ipasn.dat
