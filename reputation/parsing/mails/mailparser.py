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
    Mail parser, directly called by the parsing routine. This parser
    relies on e-mail readers.
"""

import base64
import imaplib
import time
from config import settings
from parsing.mails.mailfactory import MailReaderFactory
from parsing.parser import Parser
from utils.logger import LOGGER


class MailParser(Parser):
    """
        Implementation of :py:class:`parsing.parser.Parser` dedicated to mail polling & parsing.
    """

    def __init__(self):
        """
            Constructor in charge of connecting to mailbox via IMAPS.
        """
        Parser.__init__(self)

        self._imap = imaplib.IMAP4_SSL(settings.SCORING_EMAIL['host'])
        self._imap.login(settings.SCORING_EMAIL['polling']['user'], settings.SCORING_EMAIL['polling']['password'])
        self._imap.select('INBOX')

        self._failed_uids = []
        self._parser = None
        self._current = 0

        self._feed_queue(True)

    def _feed_queue(self, first_call=False):
        """
            Read the next enqueued e-mails.

            :param bool first_call: Whether this is the first time this method is called (default False)
        """
        if not first_call:
            self._delete_messages()

        self._queue = []
        self._uids = []
        self._current = 0

        while not len(self._queue):
            _, data = self._imap.search(None, 'ALL')
            uids = data[0].split()
            msg_pack = uids[:10] if len(uids) > 10 else uids
            for num in msg_pack:
                # Skip mails that previously failed
                if num in self._failed_uids:
                    continue

                _, raw_msg = self._imap.fetch(num, '(RFC822)')
                self._queue.append(raw_msg[0][1])
                self._uids.append(num)

            if not len(self._queue):
                LOGGER.debug('No email retrieved. Waiting before retrying.')
                time.sleep(10)

    def _delete_messages(self):
        """
            Remove from inbox parsed e-mails.
        """
        for num in self._uids:
            self._imap.store(num, '+FLAGS', '\\Deleted')

        self._imap.expunge()

    def next(self):
        if self._current >= len(self._queue):
            self._feed_queue()

        res = self._queue[self._current].decode()

        LOGGER.debug('Parsing mail...')
        try:
            self._parser = MailReaderFactory.get_reader_for_mail(res)
            self._current = self._current + 1
        except Exception as ex:
            LOGGER.error('Error while parsing mail #%s', self._uids[self._current])
            LOGGER.error('Unable to determine source of this mail (raw content follows): %s', ex)
            LOGGER.error('Retrieved email:\n%s', res)

            LOGGER.debug('-- Recovery mode --')
            # Add this uid to the failed list so don't retry to parse this mail anymore
            self._failed_uids.append(self._uids[self._current])
            # Remove uid from the list so this email won't be deleted.
            self._uids.remove(self._uids[self._current])
            # Remove mail from the queue
            self._queue.remove(self._queue[self._current])

            LOGGER.debug('Ok. Now, try to fetch another mail...')

            # Try to fetch next mail one more time...
            return self.next()

        return res

    def close(self):
        self._imap.close()
        self._imap.logout()

    def get_raw(self, data):
        return base64.b64encode(data)

    def compute_weight(self, data):
        return self._parser.compute_weight()

    def get_date(self, data):
        return self._parser.get_date()

    def get_source(self, data):
        return self._parser.get_source()

    def get_ip(self, data):
        return self._parser.get_ip()

    @staticmethod
    def get_description():
        """ Mandatory method for auto-registration """
        return [{
            'name': 'AOL',
        }, {
            'name': 'SignalSpam',
            'shortened': 'SGS'
        }, {
            'name': 'SpamCop',
            'shortened': 'SCOP'
        }]
