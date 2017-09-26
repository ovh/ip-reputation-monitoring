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
#

"""
    Spamhaus API service.
"""

from time import mktime
from db import db


def get_spamhaus_entries(is_active):
    """
        Retrive from DB spamhaus entry, active or not.
    """
    # Query DB
    with db.DB() as database:
        documents = database.find_spamhaus_entries(is_active)
        if not documents:
            return None

    # Format dto
    result = []
    for doc in documents:
        result.append({
            'sblNumber': doc['sbl_number'],
            'cidr': doc['cidr'],
            'firstSeen': int(mktime(doc['first_seen'].timetuple())),
            'lastSeen': int(mktime(doc['last_seen'].timetuple()))
        })

    return result
