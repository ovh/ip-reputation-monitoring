# -*- coding: utf-8 -*-
#
# Copyright (C) 2016, OVH SAS
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

""" Reporting module """

import smtplib
from email.mime.text import MIMEText
from config import settings
from db import db
from utils import utils
from utils.logger import LOGGER


MAIL_CATEGORY = 'SPAM'


class Reporter(object):
    """
        Class used to send an e-mail notification for each IP ranked as
        having the worst reputation.
    """

    def __init__(self):
        pass

    def send_reports(self):
        """
            The only public method used to run the process of email sending.
        """
        with db.DB() as database:
            for entry in database.find_highest_scores():
                subject = self._prepare_subject(entry['_id'], entry['value'])

                raw = self._prepare_raw(database, entry['_id'])
                body = self._prepare_body(entry['_id'], entry['value'], raw)

                self._send_mail(subject, body)

    def _send_mail(self, subject, body):
        """
            Send a simple text e-mail. Settings are used to get the recipient.

            :param str subject: Subject of the email
            :param str body: Body content of the email
        """
        try:
            msg = MIMEText(body)

            msg['Subject'] = subject
            msg['From'] = settings.SCORING_EMAIL['reporting']['from']
            msg['To'] = settings.SCORING_EMAIL['reporting']['to']

            smtp = smtplib.SMTP_SSL(settings.SCORING_EMAIL['host'])
            smtp.sendmail(msg['From'], msg['To'], msg.as_string())
            smtp.quit()
        except Exception as ex:
            LOGGER.error('Something went wrong when sending the email: %s', ex)

    def _prepare_raw(self, database, addr):
        """
            Retrieve raw data that triggered new event to be attached to this ip addr
            (it can take the form of a csv line or an email).

            :param database: The DB instance
            :param str addr: Related IP address
            :rtype array:
            :return: Array of raw data for each event entry
        """
        results = []
        for entry in database.find_all_event_data_for_ip(addr):
            line = "Raised by {} with a weight of {}.".format(entry['source'], str(entry['weight']))

            # Emails are encoded as b64 to avoid any side effects.
            if not utils.is_base64_encoded(entry['data']):
                line = "{} Raw data:\n{}".format(line, entry['data'])
            else:
                line = "{} This is an e-mail and it won't be displayed in this report.".format(line)

            results.append(line)

        return results

    def _prepare_subject(self, addr, score):
        """ Format email subject """
        return "{} [score={}]".format(addr, str(score))

    def _prepare_body(self, addr, score, raw):
        """ Format email body """
        lines = []

        lines.append(' '.join(['IP:', addr]))
        lines.append(' '.join(['Category:', MAIL_CATEGORY]))
        lines.append(' '.join(['Score:', str(score), '(', self._get_grade(score), ')']))
        lines.append('')
        lines.append('')

        if len(raw) > 250:
            lines.append(' '.join(['Find below 250 of the', str(len(raw)), 'entries for this IP:']))
            lines.extend(raw[:250])
        else:
            lines.append(' '.join(['Find below the', str(len(raw)), 'entries for this IP:']))
            lines.extend(raw)

        return '\n'.join(lines)

    def _get_grade(self, score):
        """ Associate a label to a score """
        if score > 10000:
            return 'APOCALYPSE'
        elif score > 5000:
            return 'ABSOLUTELY CRITICAL'
        elif score > 2000:
            return 'CRITICAL'
        elif score > 500:
            return 'MAJOR'
        elif score > 250:
            return 'MINOR'
        elif score > 0:
            return 'NOT RELEVANT'
        else:
            return 'NOP'
