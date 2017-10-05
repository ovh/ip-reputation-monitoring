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
    ARF e-mail reader
"""

import re
import time
from datetime import datetime
from email.utils import parsedate_tz, mktime_tz
from parsing.mails.mailreader import AbstractMailReader


class ArfReader(AbstractMailReader):
    """
        Reader dedicated to read ARF formatted reports (i.e. : AOL, SignalSpam, ...)
    """

    def __init__(self, raw, source):
        AbstractMailReader.__init__(self)
        self._source = source
        self._data = raw

    def compute_weight(self):
        match = re.search(r'Received-Date:\s(.*)', self._data)
        if not match:
            return 1

        # Check whether effective reception date is old or not (old = > 3d)
        timestamp = mktime_tz(parsedate_tz(match.group(1)))
        timestamp = timestamp + 3 * 24 * 60 * 60

        return 0 if timestamp < time.time() else 1

    def get_date(self):
        match = re.search(r'Date:\s(.*)', self._data)
        if not match:
            return datetime.now()

        timestamp = mktime_tz(parsedate_tz(match.group(1)))
        return datetime.utcfromtimestamp(timestamp)

    def get_source(self):
        return self._source

    def get_ip(self):
        match = re.search(r'Source-IP:\s(.*)', self._data)
        if not match:
            return None

        return match.group(1).strip()
