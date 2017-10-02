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

""" Everything you need to deal with the databases is here. """
import time
from datetime import datetime

import psycopg2
from psycopg2 import extras
from config import settings


class Postgres(object):
    """
        This class is designed to provide everything needed to deal with postgres
        In other words, this class is a typical data access object.
    """

    def __enter__(self):
        self._open()
        return self

    def __exit__(self, type_exc, value, traceback):
        self._close()
        return False

    def _open(self):
        """
            Open connection to PostgreSQL
        """
        ssl = 'require' if settings.SPAMHAUS_DB['secured'] else None
        self._connection = psycopg2.connect(database=settings.SPAMHAUS_DB['db'],
                                            user=settings.SPAMHAUS_DB['user'],
                                            password=settings.SPAMHAUS_DB['password'],
                                            host=settings.SPAMHAUS_DB['host'],
                                            port=settings.SPAMHAUS_DB['port'],
                                            sslmode=ssl)
        self._cursor = self._connection.cursor(cursor_factory=extras.DictCursor)

    def _close(self):
        """ Close db's connection. """
        self._connection.close()

    def update_spamhaus_entries(self, documents):
        """
            Update or insert a spamhaus entry into the spamhaus table. For each entry that
            is no longer active, update them to set their attr `active` to false.

            :param list documents: List of dictionaries representing documents to upsert having at least
            those mandatory keys: [sbl_number, cidr]
        """
        now = datetime.now()

        # First upsert still active entries
        for document in documents:
            self._cursor.execute("INSERT INTO spamhaus (sbl_number, cidr) "
                                 "VALUES (%(sbl_number)s, %(cidr)s) "
                                 "ON CONFLICT (sbl_number) DO UPDATE SET "
                                 "   last_seen = %(now)s,"
                                 "   active = TRUE",
                                 {
                                     "sbl_number": document['sbl_number'],
                                     "cidr": document['cidr'],
                                     "now": now
                                 })

        # Now, set inactive all active documents that are not in documents
        active_ids = [doc['sbl_number'] for doc in documents]
        self._cursor.execute("UPDATE spamhaus "
                             "SET active = FALSE "
                             "WHERE active = TRUE AND sbl_number NOT IN %(actives)s",
                             {
                                 "active": tuple(active_ids)
                             })

        self._connection.commit()

    def find_spamhaus_entries(self, is_active=None):
        """
            Retrieve all registered spamhaus tickets.

            :param bool is_active: (Optional) Filter tickets depending if they're still active or not.
            :rtype: cursor
            :return: All desired spamhaus tickets sorted by first_seen date (asc)
        """
        if is_active is None:
            self._cursor.execute("SELECT * FROM spamhaus "
                                 "ORDER BY first_seen ASC")
            return self._cursor.fetchall()

        self._cursor.execute("SELECT * FROM spamhaus "
                             "WHERE active = %(active)s "
                             "ORDER BY first_seen ASC",
                             {
                                 "active": is_active
                             })
        return self._cursor.fetchall()
