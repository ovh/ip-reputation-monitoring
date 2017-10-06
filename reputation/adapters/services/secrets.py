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

""" Abstraction of a secrets service. """

import abc


class SecretsServiceException(Exception):
    """
        Exception that must be raised by SecretsService implementations
        to ensure error are correctly handled.
    """
    pass


class SecretsServiceBase(object):
    """
        Interface defining a secrets service used to fetch application secrets.
        For example, an implementation might get these secrets from the env variables, or from vault.

        The only exception allowed to be raised is :py:exc:`SecretServiceException`
    """

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def __enter__(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def __exit__(self, exc_type, value, traceback):
        raise NotImplementedError()

    @abc.abstractmethod
    def read(self, variable_name):
        """
            Read an existing secret.

            :param str variable_name: Variable name to be read
            :return:  Content of the variable
            :raises SecretsServiceException: if any error occur (ie: secret cannot be found)
        """
        raise NotImplementedError()
