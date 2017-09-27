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
    CleanTalk CSV parser.
    Notice, the csv is produced by the HTML to CSV tool provided.
"""

from datetime import datetime
from parsing.csv.csvparser import CSVParser

PARSER_NAME = 'CleanTalk'


class CleanTalkParser(CSVParser):
    """
        CleanTalk dedicated csv parser
    """

    def __init__(self, path):
        CSVParser.__init__(self, path, ',')

    def compute_weight(self, data):
        return float(data[3]) / 10 if data[3] else 1

    def get_date(self, data):
        return datetime.strptime(data[2], '%Y-%m-%d %H:%M:%S') if data[2] else datetime.now()

    def get_source(self, data):
        return PARSER_NAME

    def get_ip(self, data):
        return data[0]

    @staticmethod
    def get_description():
        """ Mandatory method for auto-registration """
        return {
            'name': PARSER_NAME,
            'shortened': 'CTALK'
        }
