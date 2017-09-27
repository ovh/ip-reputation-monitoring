#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Spamhaus service unit tests """

import unittest
from datetime import datetime
from time import mktime
from mock import patch
from api.services import spamhaus


class TestSpamhausService(unittest.TestCase):
    """ Spamhaus service unit tests """

    def test_spamhaus_active_entries(self):
        now = datetime.now()
        last_year = now.replace(year=now.year - 1)

        with patch('db.postgres.Postgres') as mock:
            instance = mock.return_value
            enter = instance.__enter__.return_value
            enter.find_spamhaus_entries.return_value = [{
                'active': True,
                'sbl_number': 1,
                'first_seen': last_year,
                'last_seen': now,
                'cidr': '1.2.3.4/32'
            }]

            expected = [{
                'sblNumber': 1,
                'firstSeen': int(mktime(last_year.timetuple())),
                'lastSeen': int(mktime(now.timetuple())),
                'cidr': '1.2.3.4/32'
            }]

            result = spamhaus.get_spamhaus_entries(True)

            enter.find_spamhaus_entries.assert_called_with(True)

            self.assertEqual(1, len(result))
            self.assertEqual(expected, result)
