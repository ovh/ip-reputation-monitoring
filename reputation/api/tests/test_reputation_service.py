#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Reputation service unit tests """

import unittest
from mock import patch
from api.services import reputation
from parsing.registered import parsers, shortened_names


class TestReputationServices(unittest.TestCase):
    """ Reputation service unit tests """

    def test_reputation_events_for_source(self):
        with patch('db.mongo.Mongo') as mock:
            instance = mock.return_value
            enter = instance.__enter__.return_value
            enter.find_all_event_data_for_ip.return_value = [
                {'weight': 3, 'timestamp': 4, 'filename': 'ZZZ', 'source': 'SpamCop', 'data': 'AAA'},
                {'weight': 5, 'timestamp': 5, 'filename': 'YYY', 'source': 'SpamCop', 'data': 'BBB'},
                {'weight': 7, 'timestamp': 6, 'filename': 'XXX', 'source': 'AOL', 'data': 'CCC'}       # NOP SOURCE
            ]

            result = reputation.get_reputation_events_for_source('5.5.5.5', shortened_names['SpamCop'], 3)

            enter.find_all_event_data_for_ip.assert_called_with('5.5.5.5', 3, True)

            self.assertEquals(2, len(result))
            self.assertEqual(['YYY', 'ZZZ'], sorted([r['filename'] for r in result]))

    def test_reputation_events_for_source_b64(self):
        with patch('db.mongo.Mongo') as mock:
            instance = mock.return_value
            enter = instance.__enter__.return_value
            enter.find_all_event_data_for_ip.return_value = [
                {'weight': 3, 'timestamp': 4, 'filename': 'ZZZ', 'source': 'SpamCop', 'data': 'AAA'},  # NOP SOURCE
                {'weight': 7, 'timestamp': 5, 'filename': 'XXX', 'source': 'AOL', 'data': 'SGVsbG8gd29ybGQ='}
            ]

            result = reputation.get_reputation_events_for_source('5.5.5.5', 'AOL', 3)

            enter.find_all_event_data_for_ip.assert_called_with('5.5.5.5', 3, True)

            self.assertEquals(1, len(result))
            self.assertEqual("Hello world", result[0]['data'])

    def test_aggregated_reputation(self):
        with patch('db.mongo.Mongo') as mock:
            instance = mock.return_value
            enter = instance.__enter__.return_value
            enter.find_all_events_for_ip.return_value = [
                {'weight': 3, 'timestamp': 4, 'filename': 'ZZZ', 'source': 'SpamCop', 'data': 'AAA'},
                {'weight': 5, 'timestamp': 5, 'filename': 'YYY', 'source': 'SpamCop', 'data': 'BBB'},
                {'weight': 7, 'timestamp': 6, 'filename': 'XXX', 'source': 'AOL', 'data': 'CCC'}
            ]

            result = reputation.aggregate_reputation_per_source('5.5.5.5', 3)

            enter.find_all_events_for_ip.assert_called_with('5.5.5.5', 3, True)

            # Build expected values that should be all parser shortened names = 0, except SpamCop (SCOP) = 8 and AOL = 7.
            expected = []
            for parser in parsers.keys():
                weight = 0
                if parser == 'AOL':
                    weight = 7
                elif parser == 'SpamCop':
                    weight = 8

                expected.append({
                    'short_name': shortened_names[parser],
                    'full_name': parser,
                    'result': weight,
                })

            # Assertions
            self.assertEquals(len(expected), len(result))
            self.assertEqual(expected, result)
