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
    Reputation controller. Allow user to query stored data.
"""

from flask import Blueprint, request
from api.decorators.json import as_json
from api.services import reputation as reputation_service

reputation = Blueprint('reputation', __name__)


@reputation.route('/<addr>', methods=['GET'])
@as_json
def get_reputation_per_source(addr):
    """
        Retrieve aggregated weights per source for a single ip. A timestamp
        can be passed (add `start_date` parameter) so weights are computed after
        provided date.
    """
    try:
        start_date = _get_start_date()
    except:
        return {"error": "Expected start_date to be an integer."}, 400

    return reputation_service.aggregate_reputation_per_source(addr, start_date), 200


@reputation.route('/<addr>/details/<source>', methods=['GET'])
@as_json
def get_reputation_details_for_source(addr, source):
    """
        Retrieve details about events for a given source and a given ip.
        Those details consist in an array of events and for each event,
        the raw data that created this event. A timestamp can be passed
        using `start_date` parameter.
    """
    try:
        start_date = _get_start_date()
    except:
        return {"error": "Expected start_date to be an integer."}, 400

    return reputation_service.get_reputation_events_for_source(addr, source, start_date), 200


def _get_start_date():
    """
        Retrieve optionnal start date parameter and check it is valid (= a timestamp).

        :rtype: int
        :return: The start_date parameter as a timestamp
        :raises ValueError: Raised if timestamp is negative.
    """
    start_date = request.args.get('start_date', None)

    if start_date:
        start_date = int(start_date)
        if start_date < 0:
            raise ValueError()
    else:
        start_date = 0

    return start_date
