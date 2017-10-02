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

""" Global solution settings """

import logging

from config import secret_manager

#: Tells the app which implementations to load
CUSTOM_IMPLEMENTATIONS = (
    "default.adapters.services.storage.FilesystemStorageService",
)

#: Network ip to be kept while parsing
MANAGED_IPS_LIST = "./config/ips.list"
#: RBL storage context which pass the context to the :py:class:`adapters.services.storage.StorageServiceBase` implementation.
RBL_STORAGE_CONTEXT = 'rbl_archives'

LOGGER = {
    'name': 'reputation',
    'level': logging.INFO,
}

#: DB settings
MONGO_DB = {
    'host': secret_manager.secrets['MONGO_HOST'],
    'port': secret_manager.secrets['MONGO_PORT'],
    'db': secret_manager.secrets['MONGO_DB'],
    'user': secret_manager.secrets['MONGO_USER'],
    'password': secret_manager.secrets['MONGO_PASSWORD'],
    'secured': True
}
SPAMHAUS_DB = {
    'host': secret_manager.secrets['POSTGRES_HOST'],
    'port': secret_manager.secrets['POSTGRES_PORT'],
    'db': secret_manager.secrets['POSTGRES_DB'],
    'user': secret_manager.secrets['POSTGRES_USER'],
    'password': secret_manager.secrets['POSTGRES_PASSWORD'],
    'secured': True
}

#: Global Email settings (inbox creds, header and reporting)
SCORING_EMAIL = {
    'host': secret_manager.secrets['EMAIL_HOST'],
    'reporting': {
        'from': secret_manager.secrets['REPORTING_SENDER'],
        'to': secret_manager.secrets['REPORTING_TARGET']
    },
    'polling': {
        'user': secret_manager.secrets['FBL_USER'],
        'password': secret_manager.secrets['FBL_PASSWORD']
    },
    'partner_header': secret_manager.secrets['FBL_PARTNER_HEADER']
}

#: Flask configuration
API = {
    'host': '0.0.0.0',
    'port': 5000,
    'debug': False
}
