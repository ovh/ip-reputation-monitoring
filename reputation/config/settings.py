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

""" Customizable settings """

import logging

#: Tells the app which implementations to load
CUSTOM_IMPLEMENTATIONS = (
    "default.adapters.services.storage.FilesystemStorageService",
    "default.adapters.services.secrets.EnvironmentSecretService",
)

#: Network ip to be kept while parsing
MANAGED_IPS_LIST = "./config/ips.list"

#: RBL storage context which pass the context to the
# :py:class:`adapters.services.storage.StorageServiceBase` implementation.
RBL_STORAGE_CONTEXT = 'rbl_archives'

LOGGER = {
    'name': 'reputation',
    'level': logging.INFO,
}

#: Flask configuration
API = {
    'host': '0.0.0.0',
    'port': 5000,
    'debug': False
}
