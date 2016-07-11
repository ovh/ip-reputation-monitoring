# -*- coding: utf-8 -*-
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

"""
    Extract Spamhaus blacklisted IPs from their raw HTML page.
"""

import sys
from datetime import datetime
import bs4
from mongo import mongo
from utils import utils
from utils.logger import LOGGER

SBL_STRING = 'SBL'
TAG_TO_FIND = [
    'table',
    {
        'cellspacing': 0,
        'cellpadding': 4,
        'border': 0,
        'width': '100%'
    }
]


class UnrecognizedFormatException(Exception):
    """ Custom exception raised if page format is not recognized as valid. """
    pass


def parse_html(content):
    """
        Parse Spamhaus HTML webpage to extract opened tickets.

        :param str content: Raw html sources
        :raises UnrecognizedFormatException: If sources cannot be parsed
        :rtype: array
        :return: Array of dictionnaries containing all opened SBL.
    """
    soup = bs4.BeautifulSoup(content)
    search = soup.find_all(*TAG_TO_FIND)

    if not search:
        raise UnrecognizedFormatException("Cannot parse file.")

    result = []
    # Iterate through the found rows
    for row in search:
        # sbl_number and CIDR are surrounded by a bold tag.
        sbl_number = cidr = None
        infos = [elem.text for elem in row.find_all('b')]
        for info in infos:
            if info.startswith(SBL_STRING):
                sbl_number = int(info.replace(SBL_STRING, ''))
            elif '/' in info:
                addr = info.split('/')[0]
                if utils.is_valid_ipv4_address(addr):
                    cidr = info

        first_seen = row.find_all('td')[4].find_all('span')[0].text
        first_seen = datetime.strptime(first_seen, '%d-%b-%Y %H:%M GMT')

        if all((sbl_number, first_seen, cidr)):
            result.append({
                'sbl_number': sbl_number,
                'first_seen': first_seen,
                'cidr': cidr
            })

    return result


def update_db(documents):
    """
        Update MongoDB by inserting new entries or updating existing ones (last seen
        date, is it still active, etc.)

        :param tuple documents: A tuple of dict containing documents to upsert.
    """
    with mongo.Mongo() as database:
        database.update_spamhaus_entries(documents)


def main():
    """
        Spamhaus blacklisted ip extracting tool entry point.
    """
    LOGGER.info("Started...")

    # Read from stdin data
    buf = []
    for line in sys.stdin:
        buf.append(line)

    content = '\n'.join(buf)

    LOGGER.info("Parsing html (%d bytes)", len(content))
    documents = parse_html(content)
    LOGGER.info("%d spamhaus entries found.", len(documents))

    LOGGER.info("Updating database.")
    update_db(documents)

    LOGGER.info("Done.")
