
import os
import unittest
from datetime import datetime
from tools.spamhaus import spamhaus


class TestSpamhaus(unittest.TestCase):

    def test_parser(self):
        basedir = os.path.dirname(__file__)
        with open(os.path.join(basedir, 'sample_sbl.html')) as f:
            content = f.read()

        documents = spamhaus.parse_html(content)

        self.assertEqual(33, len(documents))

        expected_document_keys = ['sbl_number', 'first_seen', 'cidr']
        for doc in documents:
            self.assertTrue(all(key in doc for key in expected_document_keys))

        expected_document = {
            'sbl_number': 284491,
            'cause': "servicetob.net / 'alexandra besson' (sources)",
            'first_seen': datetime(2016, 1, 28, 23, 30),
            'cidr': '5.39.124.160/27'
        }

        self.assertEqual(expected_document, documents[11])
