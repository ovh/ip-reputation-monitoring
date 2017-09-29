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

"""
    Spamhaus controller
"""

from flask import Blueprint
from api.decorators.json import as_json
from api.services import spamhaus as spamhaus_service

spamhaus = Blueprint('spamhaus', __name__)


@spamhaus.route('/active', methods=['GET'])
def get_spamhaus_active_entries():
    """
        Endpoint dedicated to retrieve active spamhaus entries.
    """
    return _retrieve_entries(True)


@spamhaus.route('/resolved', methods=['GET'])
def get_spamhaus_resolved_entries():
    """
        Endpoint dedicated to retrieve resolved spamhaus entries.
    """
    return _retrieve_entries(False)


@as_json
def _retrieve_entries(is_active):
    """ Handy function which avoid code duplication """
    result = spamhaus_service.get_spamhaus_entries(is_active)
    if result is None:
        return {"error": "Error while fetching active spamhaus entries."}, 500

    return result, 200
