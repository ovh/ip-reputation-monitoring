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

""" Default secrets implementation using environment variables. """

import os
from adapters.services import secrets


class EnvironmentSecretService(secrets.SecretsServiceBase):
    """
        Implementation of the :py:class:`adapters.services.secrets.SecretsServiceBase` interface
        to provide a secrets service using environment variables.
    """

    def __enter__(self):
        """
            Fetches the secrets and store them in the environment variables.
            For this implementation, the secrets are already in the environment, so we do nothing
        """
        return self

    def __exit__(self, type_exc, value, traceback):
        pass

    def read(self, variable_name):
        """
            Read an existing file.

            :param str variable_name: Variable name to be read
            :return:  Content of the variable
            :raises SecretsServiceException: if any error occur (ie: secret cannot be found)
        """
        try:
            res = os.getenv(variable_name)
            if res is None:
                raise Exception("Secret with name '{}' not found in environment".format(variable_name))

            return res
        except Exception as exc:
            raise secrets.SecretsServiceException(exc)
