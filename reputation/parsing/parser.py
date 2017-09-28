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

""" Parser main routine and abstraction. """

import abc
import time
import traceback
from datetime import datetime, timedelta
from db import db
from utils import utils
from utils.logger import LOGGER


def _get_yesterday_date(now):
    delta = timedelta(days=1)
    yesterday = now - delta
    return int(time.mktime(yesterday.timetuple()))


# Current date - 1 day
YESTERDAY = _get_yesterday_date(datetime.now().date())


class Parser(object):
    """
        Abstract class that must be implemented by each RBL/FBL parser.
    """

    __metaclass__ = abc.ABCMeta

    def __init__(self):
        pass

    @abc.abstractmethod
    def next(self):
        """
            Used when iterating over the object to parse.

            :rtype: Object
            :return: Next object to handle or `None` if program can exit.
        """
        return None

    @abc.abstractmethod
    def close(self):
        """ Cleanup method when exiting  """
        pass

    @abc.abstractmethod
    def compute_weight(self, data):
        """
            Compute weight for the current object being treated

            :param str data: Data of the current handled object
            :rtype: int
            :return: Weight of this entry
        """
        return -1

    @abc.abstractmethod
    def get_ip(self, data):
        """
            Get IP of the current entry.

            :param str data: Data of the current handled object
            :rtype: str
            :return: IP of the current entry
        """
        return None

    @abc.abstractmethod
    def get_source(self, data):
        """
            Get the source of this entry (i.e.: SNDS, SpamCop, ...)

            :param str data: Data of the current handled object
            :rtype: str
            :return: Source of this entry
        """
        return None

    @abc.abstractmethod
    def get_date(self, data):
        """
            Get the date of this entry

            :param str data: Data of the current handled object
            :rtype: int
            :return: Timestamp corresponding to the date of this entry
        """
        return None

    @abc.abstractmethod
    def get_raw(self, data):
        """
            Get raw entry, as it was before having been parsed.

            :param str data: Data of the current handled object
            :rtype: str
            :return: String containing the raw entry
        """
        return None

    def run(self):
        """
            Run the parser.
        """
        with db.Mongo() as database:
            current = self.next()
            while current:
                try:
                    addr = self.get_ip(current)
                    if not addr:
                        LOGGER.info('Entry skipped because no specified IP.')
                        current = self.next()
                        continue

                    if not utils.is_managed_ip(addr):
                        LOGGER.debug('Not a managed IP [%s].', addr)
                        current = self.next()
                        continue

                    doc_ts = int(time.mktime(self.get_date(current).timetuple()))
                    if doc_ts < YESTERDAY:
                        LOGGER.debug('This entry is too old [%s].', self.get_date(current))
                        current = self.next()
                        continue

                    document = {
                        'ip': addr,
                        'timestamp': doc_ts,
                        'weight': self.compute_weight(current),
                        'source': self.get_source(current),
                        'raw': self.get_raw(current)
                    }
                    database.push_ip_document(document)
                except Exception as exc:
                    LOGGER.error('Unexpected error: %s [%s]', type(exc), exc.message)
                    LOGGER.error(traceback.format_exc())

                current = self.next()
            self.close()
