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
    Reputation API service. Query DB and build DTOs.
"""

from db import mongo
from parsing.registered import parsers, shortened_names
from utils import utils
import base64


def aggregate_reputation_per_source(addr, start_date):
    """
        Aggregate ip reputation per source returning for each source
        the sum of the weights.

        :param str addr: Ip the reputation must be computed with
        :param int start_date: Timestamp the events must be retrieved from
        :rtype: dict
        :return: dictionary that gives for each source, the aggregated
            weight
    """
    with mongo.Mongo() as database:
        events = database.find_all_events_for_ip(addr, start_date, True)

    # Reduce by source
    scores_by_source = _compute_score_by_source(events)

    # Append sources which are missing in scores_by_source (no attached events)
    for parser in parsers.keys():
        if parser not in scores_by_source.keys():
            scores_by_source[parser] = 0

    # Format final dto
    result = []
    for source in scores_by_source.keys():
        if source not in shortened_names.keys():
            short_name = source
        else:
            short_name = shortened_names[source]

        result.append({
            'short_name': short_name,
            'full_name': source,
            'result': scores_by_source[source],
        })

    return result


def get_reputation_events_for_source(addr, source, start_date):
    """
        Get reputation events with full data (raw data included) for
        a given ip and a given source.

        :param str addr: Ip the reputation must be computed with
        :param str source: Source short name to get events of
        :param int start_date: Timestamp the events must be retrieved from
        :rtype: array
        :return: Array of events
    """
    with mongo.Mongo() as database:
        events = database.find_all_event_data_for_ip(addr, start_date, True)

    result = [event for event in events if event['source'] == _map_source_from_shortname(source)]

    # Find the first data to determine whether data are b64 encoded or not.
    is_encoded = False
    for event in result:
        if event['data']:
            is_encoded = utils.is_base64_encoded(event['data'])
            break

    # If data are encoded, then decode all
    if is_encoded:
        for event in result:
            event['data'] = base64.b64decode(event['data']).decode() if event['data'] else event['data']

    return result


def _compute_score_by_source(events):
    result = {}
    for event in events:
        if event['source'] in result.keys():
            result[event['source']] = result[event['source']] + event['weight']
        else:
            result[event['source']] = event['weight']

    return result


def _map_source_from_shortname(short_name):
    """
        Get source fullname from its shortname

        :param str short_name: Short name of the source
        :rtype: str
        :return: Full name of this source or `short_name` if not found
    """
    for fullname in shortened_names:
        if shortened_names[fullname] == short_name:
            return fullname

    # None found
    return short_name
