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

""" Default storage implementation using Filesystem. """

import os
from adapters.services import storage


class FilesystemStorageService(storage.StorageServiceBase):
    """
        Implementation of the :py:class:`adapters.services.storage.StorageServiceBase` interface
        to provide a storage service using the host filesystem.
    """

    def __init__(self, context):
        """
            Constructor

            :param str context: Root directory where files are stored
            :raises StorageServiceException: If root directory creation failed
        """
        self._root_dir = context

        # Check path exists else create it
        try:
            if context and not os.path.exists(context):
                os.makedirs(context)
        except Exception as exc:
            raise storage.StorageServiceException(exc)

    def __enter__(self):
        return self

    def __exit__(self, type_exc, value, traceback):
        pass

    def read(self, filename):
        """
            Read an existing file.

            :param str filename: file to read
            :rtype: raw
            :return:  Content of the file
            :raises StorageServiceException: if file does not exist
        """
        target = os.path.join(self._root_dir, filename)

        if not os.path.exists(target):
            raise storage.StorageServiceException('File does not exist.')

        try:
            with open(target, 'rb') as fdesc:
                return fdesc.read()
        except Exception as exc:
            raise storage.StorageServiceException(exc)

    def write(self, filename, data):
        """
            Write a brand new file.

            :param str filename: Filename of the file to be written
            :param raw data: Associated data (might be binary content)
            :rtype: bool
            :return: `True` if everything went ok, `False` otherwise
            :raises StorageServiceException: if any error occur
        """
        try:
            target = os.path.join(self._root_dir, filename)

            # Check whether submitted path exists else, create it.
            dirname = os.path.dirname(target)
            if dirname and not os.path.exists(dirname):
                os.makedirs(dirname)

            with open(target, 'wb') as fdesc:
                fdesc.write(data)

            return True
        except Exception as ex:
            raise storage.StorageServiceException(ex)

    def delete(self, filename):
        """
            Remove an existing file.

            :param str filename: Name of the file to remove
            :raises StorageServiceException: if any error occur
        """
        try:
            target = os.path.join(self._root_dir, filename)

            if not os.path.exists(target):
                raise storage.StorageServiceException("File not found.")

            os.remove(target)
        except Exception as ex:
            raise storage.StorageServiceException(ex)
