#
# Copyright (C) 2017, OVH SAS
#
# This file is part of ip-reputation-monitoring.
#
# ip-reputation-monitoring is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
    Factory dedicated to :py:class:`parsing.mails.mailreader.AbstractMailReader`
    instantiation.
"""

import re
from config import settings
from parsing.mails import arf, spamcop
from utils.logger import LOGGER


class MailReaderFactory(object):
    """
        Factory returning a :py:class:`parsing.mails.mailreader.AbstractMailReader`
        instance able to read a received email.
    """
    def __init__(self):
        raise RuntimeError("MailReaderFactory is not designed to be instantiated.")

    @staticmethod
    def get_reader_for_mail(raw):
        """
            Automatically detect the appropriate reader that will be able to
            read the passed e-mail. This method is static.

            :param str raw: The raw e-mail content
            :rtype: Object
            :return: An instance of :py:class:`parsing.mails.mailreader.AbstractMailReader`
        """
        match = re.search(r'{}:\s(.*)'.format(settings.SCORING_EMAIL['partner_header']), raw)
        if not match:
            raise Exception('Malformed input mail :: missing header [{}]'.format(settings.SCORING_EMAIL['partner_header']))

        source = match.group(1).strip()

        LOGGER.debug('Mail from %s', source)
        if source in ("AOL", "SignalSpam"):
            return arf.ArfReader(raw, source)
        elif source == "SpamCop":
            return spamcop.SpamcopReader(raw)

        raise Exception(
            'Malformed input mail :: unknown value [{}] for header [{}]'.format(source, settings.SCORING_EMAIL['partner_header'])
        )
