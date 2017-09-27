#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Blacklist service unit tests """

import unittest
from api.services import blacklist
from config.dnsbl import DNS_BL


class TestBlacklistServices(unittest.TestCase):
    """ Blacklist service unit tests """

    def test_check_rbl_blacklist(self):
        """ Checking OVH website IP, if it's blacklisted, that's sooooo weird ! """
        res = blacklist.get_blacklist_report('213.186.33.34')

        expected = []
        for source in DNS_BL:
            expected.append({
                'short_name': source['shortened'],
                'full_name': source['name'],
                'result': False
            })

        self.assertEqual(len(expected), len(res))
        self.assertEqual(expected, res)
