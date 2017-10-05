# pylint: disable=W0223
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
    Base definition of a CSV parser.
    This class must be implemented by every CSV parser.
"""

import abc
import csv
import os
from parsing.parser import Parser


class CSVParser(Parser):
    """
        Abstract class implementing :py:class:`parsing.parser.Parser` dedicated for CSV parsing.
    """

    __metaclass__ = abc.ABCMeta

    def __init__(self, input_file, delimiter):
        """
            Default constructor

            :param str input: Path of the CSV file to parse
            :param str delimiter: CSV delimiter
            :raises: `IOError` if an error occurs while opening the file
        """
        Parser.__init__(self)

        if not os.path.exists(input_file):
            raise IOError(str('File [{}] does not exist.'.format(input_file)))

        self._delim = delimiter
        self._current_row = 0
        with open(input_file, 'r') as fdesc:
            content = fdesc.read()
            self._rows = csv.reader(content.splitlines(), delimiter=delimiter)

    def next(self):
        try:
            return next(self._rows)
        except:
            return None

    def close(self):
        pass

    def get_raw(self, data):
        return self._delim.join(data)
