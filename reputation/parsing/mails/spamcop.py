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
    Spamcop mail reader
"""

import re
from datetime import datetime
from email.utils import parsedate_tz, mktime_tz
from parsing.mails.mailreader import AbstractMailReader


class SpamcopReader(AbstractMailReader):
    """
        Reader dedicated to read SpamCop mails.
    """

    def __init__(self, raw):
        AbstractMailReader.__init__(self)
        self._data = raw

    def compute_weight(self):
        return 20

    def get_date(self):
        match = re.search(r'Date:\s(.*)', self._data)
        if not match or not match.group(1):
            return datetime.now()

        timestamp = mktime_tz(parsedate_tz(match.group(1)))
        return datetime.utcfromtimestamp(timestamp)

    def get_source(self):
        return 'SpamCop'

    def get_ip(self):
        match = re.search(
            r'Subject: .*SpamCop \(([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})\)',
            self._data
        )

        if not match or not match.group(1):
            return None

        return match.group(1).strip()
