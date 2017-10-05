
import os
import unittest
from tools.cleantalk import ct_formatter


class TestCleanTalkFormatter(unittest.TestCase):

    def test_formatter(self):
        basedir = os.path.dirname(__file__)
        with open(os.path.join(basedir, 'sample_ct.html')) as f:
            content = f.read()

        cells = ct_formatter.parse_html(content)

        self.assertEqual(2, len(cells))
        self.check_cells(cells[0], ('aa.aaa.aa.aaa', '2016-01-12 09:08:57', '2016-01-12 20:53:03', '3'))
        self.check_cells(cells[1], ('b.bbb.bb.bb', '2016-01-12 04:26:40', '2016-01-12 20:38:49', '5'))

    def check_cells(self, cells, expected_values):
        self.assertEqual(4, len(cells))
        for i in range(len(expected_values)):
            self.assertEqual(expected_values[i], cells[i])
