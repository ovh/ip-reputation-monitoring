#!/bin/sh
#
# Copyright (C) 2016, OVH SAS
#
# This file is part of ip-reputation-monitoring.
#
# ip-reputation-monitoring is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


# RBL URL
STOP_FORUM_SPAM=http://www.stopforumspam.com/downloads/listed_ip_1_all.zip
SNDS="https://postmaster.live.com/snds/data.aspx?key=${SNDS_KEY}&days=2"
CLEANTALK=https://cleantalk.org/blacklists/AS${AS_NUMBER}
BLOCKLIST=http://lists.blocklist.de/lists/dnsbl/all.list

# User agent to get RBL with
USER_AGENT='Mozilla/5.0 (X11; Linux x86_64; rv:38.0) Gecko/20100101 Firefox/38.0 Iceweasel/38.2.0'

# Directories computation
CURRENT_DIR=`dirname \`readlink -f $0\``
REPUTATION_DIR="${CURRENT_DIR}/reputation"
OUTPUT_DIR="${CURRENT_DIR}/temp"

REPUTATION_SCRIPT="${REPUTATION_DIR}/main.py"


# Download RBL and store them in ${OUTPUT_DIR}
function download {
    >&2 echo "### Downloading files"
    date 1>&2

    cd ${OUTPUT_DIR}


    ### SFS ###
    wget ${STOP_FORUM_SPAM} -U "${USER_AGENT}" --output-document=sfs.zip  > /dev/null
    unzip sfs.zip
    rm -f sfs.zip

    mv listed*txt sfs

    ### CLEAN TALK ###
    if [ ! -z "${AS_NUMBER}" ]
    then
        wget ${CLEANTALK} -U "${USER_AGENT}" --output-document=cleantalk.html > /dev/null
        cat ${OUTPUT_DIR}/cleantalk.html | ${REPUTATION_DIR}/tools/cleantalk/ct_formatter.py > cleantalk
        rm -f ${OUTPUT_DIR}/cleantalk.html
    else
        >&2 echo "No AS_NUMBER varenv defined. Please define it to be able to fetch CleanTalk report."
    fi

    ### BLOCK LIST DE (retry until it succeed...) ###
    wget ${BLOCKLIST} -U "${USER_AGENT}" --output-document=blocklist > /dev/null
    while [ $? -ne 0 ]
    do
        wget ${BLOCKLIST} -U "${USER_AGENT}" --output-document=blocklist > /dev/null
    done

    ### SNDS (retry until it succeed...) only if you have a SNDS key ###
    if [ ! -z "${SNDS_KEY}" ]
    then
        wget "${SNDS}" -U "${USER_AGENT}" --output-document=snds > /dev/null
        while [ $? -ne 0 ]
        do
            wget "${SNDS}" -U "${USER_AGENT}" --output-document=snds > /dev/null
        done
    else
        >&2 echo "Please define your personal SNDS key in SNDS_KEY varenv to fetch live.com abuse report"
    fi


    cd ${DAT_DIR}
}

# Parse downloaded data
function parse {

    if [ ! -z "${SNDS_KEY}" ]
    then
        >&2 echo "### Parsing SNDS"
        date 1>&2
        ${REPUTATION_SCRIPT} --parse --snds "${OUTPUT_DIR}/snds"
    fi

    if [ ! -z "${AS_NUMBER}" ]
    then
        >&2 echo "###### Parsing CT"
        date 1>&2
        ${REPUTATION_SCRIPT} --parse --cleantalk "${OUTPUT_DIR}/cleantalk"
    fi

    >&2 echo "###### Parsing BL"
    date 1>&2
    ${REPUTATION_SCRIPT} --parse --blocklist "${OUTPUT_DIR}/blocklist"
    >&2 echo "###### Parsing SFS"
    date 1>&2
    ${REPUTATION_SCRIPT} --parse --stopforumspam "${OUTPUT_DIR}/sfs"
}

# Archive old entries
function purge {
    >&2 echo "### Purging Mongo"
    date 1>&2

    ${REPUTATION_SCRIPT} --purge
}

# Compute top 10 of ip with the worst reputation
function compute {
    >&2 echo "### Sending Top10"
    date 1>&2

    ${REPUTATION_SCRIPT} --scores
}

# Setting up temp dir
function setup {
    if [ ! -e "${OUTPUT_DIR}" ]
    then
        mkdir ${OUTPUT_DIR}
    fi
}

function main {

    >&2 echo "# Starting fetcher"
    date 1>&2

    setup
    download
    parse
    purge
    compute

    >&2 echo "# End fetcher"
    date 1>&2
}



main
