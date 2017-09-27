#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Main func unit tests """

import unittest
from main import get_parser_class, check_input_file
from parsing.csv import snds, cleantalk, blocklistde, stopforumspam
from parsing.mails import mailparser


class TestMain(unittest.TestCase):

    def test_get_parser_class(self):
        expected = {
            'snds': snds.SNDSParser.__name__,
            'cleantalk': cleantalk.CleanTalkParser.__name__,
            'blocklist': blocklistde.BlockListParser.__name__,
            'stopforumspam': stopforumspam.StopForumSpamParser.__name__,
            'mails': mailparser.MailParser.__name__
        }

        results = {}
        results['snds'] = get_parser_class('snds').__name__
        results['cleantalk'] = get_parser_class('cleantalk').__name__
        results['blocklist'] = get_parser_class('blocklist').__name__
        results['stopforumspam'] = get_parser_class('stopforumspam').__name__
        results['mails'] = get_parser_class('mails').__name__

        self.assertEqual(expected, results)

    def test_check_input_file(self):
        not_exists = check_input_file('/foo/bar.jsx')
        empty = check_input_file('/dev/null')
        not_empty = check_input_file('/etc/passwd')

        self.assertFalse(not_exists)
        self.assertFalse(empty)
        self.assertTrue(not_empty)
