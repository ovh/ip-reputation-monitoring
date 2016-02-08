#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Decorators unit tests """

import unittest
from flask import json
from api.decorators.json import as_json


@as_json
def test_func(to_return, code):
    return to_return, code


class TestDecorators(unittest.TestCase):
    """ Decorators unit tests """

    def test_json_decorator(self):
        method_input = {"a": 1, "b": 2}
        expected = json.dumps(method_input)

        response = test_func(method_input, 200)

        self.assertEquals(expected, response.data)
        self.assertEquals(200, response.status_code)
        self.assertEquals('application/json', response.content_type)
