#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Mail parsing unit tests """

import time
import unittest
from datetime import datetime
from config import settings
from parsing.mails.mailfactory import MailReaderFactory
from parsing.mails.mailparser import MailParser


MAILS = {
    'aol_recent': 'tests/samples/aol_recent.eml',
    'aol_old': 'tests/samples/aol_old.eml',
    'signal_spam': 'tests/samples/signal_spam.eml',
    'scop1': 'tests/samples/scop_1.eml',
    'scop2': 'tests/samples/scop_2.eml',
}


class DummyMailParser(MailParser):
    def __init__(self, mail):
        self._parser = MailReaderFactory.get_reader_for_mail(mail)


class TestMail(unittest.TestCase):

    def setUp(self):
        content = {}
        for k in MAILS.keys():
            with open(MAILS[k]) as fdesc:
                content[k] = fdesc.read()

        self._aolParser = DummyMailParser(
            content['aol_recent']
            .format(settings.SCORING_EMAIL['partner_header'], datetime.now().strftime("%a, %d %b %Y %H:%M:%S %Z"))
        )
        self._aolParser2 = DummyMailParser(content['aol_old'].format(settings.SCORING_EMAIL['partner_header']))
        self._ssmParser = DummyMailParser(content['signal_spam'].format(settings.SCORING_EMAIL['partner_header']))
        self._scopParser = DummyMailParser(content['scop1'].format(settings.SCORING_EMAIL['partner_header']))
        self._scopParser2 = DummyMailParser(content['scop2'].format(settings.SCORING_EMAIL['partner_header']))

    def test_factory_fail(self):
        self.assertRaises(Exception, DummyMailParser, 'Ceci est un mail')

    def test_get_ip(self):

        ip = self._aolParser.get_ip("")
        self.assertEqual('5.195.5.5', ip)

        ip = self._aolParser2.get_ip("")
        self.assertEqual('5.195.5.5', ip)

        ip = self._ssmParser.get_ip("")
        self.assertEqual('5.195.5.6', ip)

        ip = self._scopParser.get_ip("")
        self.assertEqual('5.195.5.7', ip)

        ip = self._scopParser2.get_ip("")
        self.assertIsNone(ip)

    def test_get_weight(self):
        weight = self._aolParser.compute_weight("")
        self.assertEqual(1, weight)

        # Old mails have no weight.
        weight = self._aolParser2.compute_weight("")
        self.assertEqual(0, weight)

        weight = self._ssmParser.compute_weight("")
        self.assertEqual(1, weight)

        weight = self._scopParser.compute_weight("")
        self.assertEqual(20, weight)

    def test_get_date(self):
        date = self._aolParser.get_date("")
        self.assertEqual(1436645680, int(time.mktime(date.timetuple())))

        date = self._aolParser2.get_date("")
        self.assertEqual(1436645680, int(time.mktime(date.timetuple())))

        date = self._ssmParser.get_date("")
        self.assertEqual(1436818480, int(time.mktime(date.timetuple())))

        date = self._scopParser.get_date("")
        self.assertEqual(1437164080, int(time.mktime(date.timetuple())))
