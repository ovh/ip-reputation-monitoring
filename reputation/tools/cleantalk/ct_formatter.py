#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (C) 2017, OVH SAS
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
    Convert CleanTalk HTML data to a nice formatted CSV :-)
"""

import sys
import bs4


def parse_html(content):
    """
        Parse CleanTalk ASN summary webpage to extract blacklisted IP.

        :param str content: Raw html sources
        :raises Exception: If sources cannot be parsed
        :rtype: array
        :return: Bi-dimensionnal array containing for each line, parsed cells.
    """
    soup = bs4.BeautifulSoup(content, 'html.parser')
    search = soup.find_all("tr")

    if not search:
        raise Exception("Cannot parse file.")

    result = []
    # Iterate through the found <tr> tags
    for value in search:
        # Retrieve cells
        raw_cells = value.find_all("td")

        # Only retains array of 5 elements (blacklisted IP)
        if len(raw_cells) != 5:
            continue

        # Format array
        cells = [item.text for item in raw_cells]

        # Remove first cell which is useless
        cells.pop(0)
        result.append(cells)

    return result


def main():
    """
        CleanTalk html to csv converter tool entry point.
    """
    # Read from stdin data
    buf = []
    for line in sys.stdin:
        buf.append(line)

    content = '\n'.join(buf)

    for cells in parse_html(content):
        print(','.join(cells))


if __name__ == "__main__":
    main()
