#!/usr/bin/env python3

""" Utils unit tests """

import base64
import time
import unittest
from datetime import datetime
from config import settings
from utils import utils


class TestUtils(unittest.TestCase):

    def test_is_base64_encoded(self):
        str1 = "Hello world !!"
        str2 = base64.b64encode(b"Hello\nWorld !!!").decode()

        self.assertFalse(utils.is_base64_encoded(str1))
        self.assertTrue(utils.is_base64_encoded(str2))

    def test_a_month_ago(self):
        now = datetime.now().date()

        if now.month == 1:
            expected = int(time.mktime(now.replace(month=12, year=now.year - 1).timetuple()))
        else:
            expected = int(time.mktime(now.replace(month=now.month - 1).timetuple()))

        self.assertEqual(expected, utils.get_a_month_ago_date())

    def test_is_managed_ip(self):
        settings.MANAGED_IPS_LIST = "tests/ips.list"

        self.assertFalse(utils.is_managed_ip("5.146.1.1"))
        self.assertTrue(utils.is_managed_ip("1.1.0.145"))

    def test_is_valid_ipv4(self):
        self.assertTrue(utils.is_valid_ipv4_address('5.5.5.5'))
        self.assertFalse(utils.is_valid_ipv4_address('5.5.5.5.5'))
        self.assertFalse(utils.is_valid_ipv4_address('127.1'))
