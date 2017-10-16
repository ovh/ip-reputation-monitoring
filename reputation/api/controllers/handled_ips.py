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
    Handled IPs controller. Exposes the list of IPs handled by the AS
"""
import os
from flask import Blueprint
from api.decorators.json import as_json

ips = Blueprint('ips_handled', __name__)


@ips.route('/', methods=['GET'])
@as_json
def get_handled_ips():
    """
        Retrieve ips handled by the AS, the IPs are fetched using the script under `reputation/config/fetch_ips.sh`
    """
    try:
        current_dir = os.path.dirname(os.path.realpath(__file__))
        ips_path = os.path.realpath(current_dir + "/../../config/ips.list")
        with open(ips_path) as f:
            ips = f.read()
    except:
        return {"error": "Couldn't find handled IPs in the server side"}, 500

    ips = ips.split('\n')
    try:
        ips.remove('')
    except ValueError:
        pass

    return ips, 200
