#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Core parser unit tests """

import unittest
from datetime import datetime
from parsing import parser


class TestParser(unittest.TestCase):

    def test_classic_yesterday(self):
        now = datetime(2015, 8, 15, 14, 30)
        res = parser._get_yesterday_date(now.date())

        yesterday = datetime.fromtimestamp(res)
        self.assertEqual(2015, yesterday.year)
        self.assertEqual(8, yesterday.month)
        self.assertEqual(14, yesterday.day)
        self.assertEqual(0, yesterday.hour)
        self.assertEqual(0, yesterday.minute)

    def test_last_day_of_year(self):
        """ Tricky case, check 2015/01/01 - 1 day == 2014/12/01 """
        now = datetime(2015, 1, 1, 14, 30)
        res = parser._get_yesterday_date(now.date())

        yesterday = datetime.fromtimestamp(res)
        self.assertEqual(2014, yesterday.year)
        self.assertEqual(12, yesterday.month)
        self.assertEqual(31, yesterday.day)
        self.assertEqual(0, yesterday.hour)
        self.assertEqual(0, yesterday.minute)
