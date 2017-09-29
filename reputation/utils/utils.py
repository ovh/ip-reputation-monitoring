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
    Handy functions
"""


import os
import socket
import time
from datetime import datetime
import netaddr
import base64
from config import settings

MANAGED_NETWORKS = []


def is_managed_ip(ip_str):
    """
        Is this IP managed by us or not?
        Check whether passed ip is managed using the file specified in setting :py:data:`config.settings.MANAGED_IPS_LIST`

        :param str ip_str: IP to test
        :rtype: bool
        :return: `True` if ip is managed by us, `False` otherwise
    """
    addr = netaddr.IPAddress(ip_str)

    if not len(MANAGED_NETWORKS):
        _read_managed_networks()

    for net in MANAGED_NETWORKS:
        if net.netmask.value & addr.value == net.value:
            return True

    return False


def _read_managed_networks():
    """ Read managed networks from :py:data:`config.setting.MANAGED_IPS_LIST` to know whether an IP must be retained or not.  """
    basedir = os.path.dirname(__file__)
    with open(os.path.join(basedir, '..', settings.MANAGED_IPS_LIST)) as fdesc:
        for line in fdesc.readlines():
            MANAGED_NETWORKS.append(netaddr.IPNetwork(line))


def is_base64_encoded(string):
    """ Tells whether the passed string is base64 encoded or not. """
    try:
        return string == base64.b64encode(base64.b64decode(string)).decode()
    except:
        return False


def get_a_month_ago_date():
    """
        Get date a month ago.

        :rtype: int
        :return: Corresponding timestamp
    """
    now = datetime.now().date()

    if now.month == 1:
        return int(time.mktime(now.replace(month=12, year=now.year - 1).timetuple()))

    return int(time.mktime(now.replace(month=now.month - 1).timetuple()))


def is_valid_ipv4_address(addr):
    """
        Check whether passed ip address is a valid IPv4 address. Shortened ip are
        considered as malformed (i.e. : 127.1)

        :param str addr: IP address to check
        :rtype: bool
        :return: True if it is a valid IPv4 address, False otherwise
    """
    try:
        socket.inet_pton(socket.AF_INET, addr)
    except AttributeError:
        # no inet_pton
        try:
            socket.inet_aton(addr)
        except socket.error:
            return False

        # Dont care about shortened ip such 127.1
        return addr.count('.') == 3
    except socket.error:
        return False

    return True
