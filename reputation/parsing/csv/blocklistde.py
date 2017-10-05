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
    Blocklist CSV parser
"""

from datetime import datetime
from parsing.csv.csvparser import CSVParser

PARSER_NAME = 'BlockList'


def compute_weight(service):
    """
        Map a service with a weight. All reported services have a
        default weight of 10, except ssh failed attempt (1), manual
        list addition (5) and the wtf category "all" (5).
    """
    return {
        'ssh': 1,
        'all': 5,
        'manually added': 5
    }.get(service, 10)


class BlockListParser(CSVParser):
    """
        Blocklist.de dedicated csv parser
    """

    def __init__(self, path):
        CSVParser.__init__(self, path, ':')

    def compute_weight(self, data):
        return compute_weight(self._get_service(data[3]))

    def get_date(self, data):
        timestamp = float(data[4].strip()[:10])
        return datetime.utcfromtimestamp(timestamp)

    def get_source(self, data):
        return PARSER_NAME

    def get_ip(self, data):
        if len(data) != 6:
            return None

        return data[0]

    def _get_service(self, cell):
        """ Try to extract service associated to the issue from a cell """
        return cell.strip().split(',')[0]

    @staticmethod
    def get_description():
        """ Mandatory method for auto-registration """
        return {
            'name': PARSER_NAME,
            'shortened': 'BLCK'
        }
