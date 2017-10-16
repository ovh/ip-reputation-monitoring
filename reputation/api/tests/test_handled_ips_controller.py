#!/usr/bin/env python3

""" Handled IPs controller unit tests """

import unittest
import os
from api.controllers import handled_ips
from flask import json, Response

temp_dir = "/tmp/pretty-random/"
ips = ["127.0.0.1/24", "92.1.0.0/4"]


class TestHandledIpsController(unittest.TestCase):
    """ Handled IPs controller unit tests """

    def setUp(self):
        current_dir = os.path.dirname(os.path.realpath(__file__))
        self.ips_path = os.path.realpath(current_dir + "/../../config/ips.list")
        with open(self.ips_path) as original_file:
            self._backup = original_file.read()

    def tearDown(self):
        with open(self.ips_path, "w") as file_to_restore:
            file_to_restore.write(self._backup)

    def test_get_handled_ips(self):
        with open(self.ips_path, "w") as f:
            f.write("\n".join(ips))

        expected = Response(
            json.dumps(ips),
            status=200,
            content_type='application/json'
        )
        result = handled_ips.get_handled_ips()

        self.assertEqual(expected.data, result.data)
        self.assertEqual(expected.status_code, result.status_code)

    def test_get_handled_ips_with_empty_line_at_the_end(self):
        with open(self.ips_path, "w") as f:
            f.write("\n".join(ips) + "\n")

        expected = Response(
            json.dumps(ips),
            status=200,
            content_type='application/json'
        )
        result = handled_ips.get_handled_ips()

        self.assertEqual(expected.data, result.data)
        self.assertEqual(expected.status_code, result.status_code)
