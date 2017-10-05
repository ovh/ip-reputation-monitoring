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
    Json related decorators.
    Notice: FlaskJSON might be better than this code but cannot install it yet.
"""

from functools import wraps
from flask import json, Response


def as_json(func):
    """ Force responses to be JSON """
    @wraps(func)
    def decorated_function(*args, **kwargs):
        """ Call wrapped function. """
        result = func(*args, **kwargs)

        assert len(result) == 2

        return Response(
            json.dumps(result[0]),
            status=result[1],
            content_type='application/json'
        )
    return decorated_function
