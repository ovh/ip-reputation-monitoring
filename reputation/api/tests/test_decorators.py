#!/usr/bin/env python3

""" Decorators unit tests """

import unittest
from flask import json
from api.decorators.json import as_json


@as_json
def _my_test_func(to_return, code):
    return to_return, code


class TestDecorators(unittest.TestCase):
    """ Decorators unit tests """

    def test_json_decorator(self):
        method_input = {"a": 1, "b": 2}
        expected = json.dumps(method_input)

        response = _my_test_func(method_input, 200)

        self.assertEqual(expected, response.data.decode())
        self.assertEqual(200, response.status_code)
        self.assertEqual('application/json', response.content_type)
