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

""" Mail reader base definition """

import abc
from utils.logger import LOGGER


class AbstractMailReader(object):
    """
        Abstract class implemented to read a single mail.
    """

    __metaclass__ = abc.ABCMeta

    def __init__(self):
        self.LOGGER = LOGGER

    @abc.abstractmethod
    def compute_weight(self):
        """
            Compute the weight of the mail being read.

            :rtype: float
            :return: Weight of the mail
        """
        return -1

    @abc.abstractmethod
    def get_ip(self):
        """
            Read concerned IP

            :rtype: str
            :return: IP the mail is talking about
        """
        return None

    @abc.abstractmethod
    def get_source(self):
        """
            Get the mail source.

            :rtype: str
            :return: Source of the mail
        """
        return None

    @abc.abstractmethod
    def get_date(self):
        """
            Get the effective date of the mail

            :rtype: int
            :return: Timestamp representing the receive date
        """
        return None
