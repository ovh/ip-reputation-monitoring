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
    Blacklist controller
"""

from flask import Blueprint
from utils import utils
from api.decorators.json import as_json
from api.services import blacklist as blacklist_service


blacklist = Blueprint('blacklist', __name__)


@blacklist.route('/<addr>', methods=['GET'])
@as_json
def check_rbl_blacklist(addr):
    """
        Check DNS BL for a given ip.
    """
    if not utils.is_valid_ipv4_address(addr):
        return {"error": "Expecting a non-shortened IPv4."}, 400

    result = blacklist_service.get_blacklist_report(addr)
    if not result:
        return {"error": "RBL queries failed."}, 500

    return result, 200
