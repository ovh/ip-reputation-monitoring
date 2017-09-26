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

""" Abstraction of a storage service. """

import abc


class StorageServiceException(Exception):
    """
        Exception that must be raised by StorageService implementations
        to ensure error are correctly handled.
    """
    pass


class StorageServiceBase(object):
    """
        Interface defining a storage service used to store documents.
        For example, an implementation might store those data in OpenStack
        Swift, a DB, RDBMS or filesystem.

        The only exception allowed to be raised is :py:exc:`StorageServiceException`
    """

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def __enter__(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def __exit__(self, exc_type, value, traceback):
        raise NotImplementedError()

    @abc.abstractmethod
    def read(self, object_name):
        """
            Read an existing object.

            :param str object_name: Unique object name to be read
            :rtype: raw
            :return:  Content of the object
            :raises StorageServiceException: if any error occur (ie: object cannot be found)
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def write(self, object_name, data):
        """
            Write a new object.

            :param str object_name: Unique object name to be pushed
            :param raw data: Associated data (might be binary content)
            :rtype: bool
            :return: `True` if everything went ok, `False` otherwise
            :raises StorageServiceException: if any error occur
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def delete(self, object_name):
        """
            Triggered when an object must be removed.

            :param str object_name: Unique object name that must be removed
            :raises StorageServiceException: if any error occur
        """
        raise NotImplementedError()
