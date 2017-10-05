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
    SNDS CSV parser
"""

from datetime import datetime
from parsing.csv.csvparser import CSVParser

THE_LIMIT = 11000.0

PARSER_NAME = 'SNDS'


def compute_base_weight(value):
    """
        Map a level with a weight multiplicator.
    """
    return {
        'GREEN': 10,
        'YELLOW': 40,
        'RED': 100
    }.get(value, 1)


class SNDSParser(CSVParser):
    """
        SNDS dedicated csv parser
    """

    def __init__(self, path):
        CSVParser.__init__(self, path, ',')

    def compute_weight(self, data):
        complain_rate = data[7]
        if not complain_rate:
            complain_rate = 1.0
        else:
            complain_rate = complain_rate.replace('<', '').replace('>', '').replace('%', '')
            complain_rate = float(complain_rate.strip()) // 2 + 0.95

        # The more there are complains and grade is bad, the more this IP will have a bad reputation
        return float(data[3]) // THE_LIMIT * float(compute_base_weight(data[6])) * complain_rate

    def get_date(self, data):
        return datetime.strptime(data[2], '%m/%d/%Y %H:%M %p') if data[2] else datetime.now()

    def get_source(self, data):
        return PARSER_NAME

    def get_ip(self, data):
        return data[0]

    @staticmethod
    def get_description():
        """ Mandatory method for auto-registration """
        return {
            'name': PARSER_NAME
        }
