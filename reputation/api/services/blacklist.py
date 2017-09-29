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
    Blacklist API service which makes the calls to the DNSBL.
"""

import socket
from config.dnsbl import DNS_BL


def get_blacklist_report(addr):
    """
        Determine whether passed ip is blacklisted amongst one of known source.

        :param str addr: IP to check
        :rtype: array
        :return: An array of dictionnaries containing for each source, the result
            (True if blacklisted, False otherwise).
    """
    result = []

    for source in DNS_BL:
        rbl_res = _is_blacklisted(source['uri'], addr)

        result.append({
            'short_name': source['shortened'],
            'full_name': source['name'],
            'result': rbl_res
        })

    return result


def _is_blacklisted(dnsbl_uri, addr):
    try:
        reversed_ip = '.'.join(addr.split('.')[::-1])
        addr = '.'.join([reversed_ip, dnsbl_uri])

        # For a given ip such 1.2.3.4, addr should look like:
        # 4.3.2.1.dnsbl_uri
        socket.gethostbyname_ex(addr)
        return True
    except (IndexError, socket.error, socket.gaierror, socket.herror, socket.timeout):
        # Not blacklisted
        return False
