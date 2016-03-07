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

""" Everything you need to dial with Mongo is here. """

import hashlib
import random
import time
from datetime import datetime

import pymongo
from bson.code import Code
from config import settings
from utils import utils
from utils.logger import LOGGER


COLLECTION_PREFIX = "dev_" if settings.MONGODB['is_dev'] else ""

IP_COLLECTION = COLLECTION_PREFIX + 'iptable'
RAW_COLLECTION = COLLECTION_PREFIX + 'rawfiles'
ARCHIVE_COLLECTION = COLLECTION_PREFIX + 'archives'
TOPTEN_COLLECTION = COLLECTION_PREFIX + 'top10'
SPAMHAUS_COLLECTION = COLLECTION_PREFIX + 'spamhaus'

A_MONTH_AGO = utils.get_a_month_ago_date()

TOP_LIMIT = 10


class Mongo(object):
    """
        This class is designed to provide everything needed to dial with mongo
        and to handle the needs of this app such as pushing new document or
        querying existing documents. In other words, this class is a typical
        data access object.
    """

    def __init__(self):
        """
            Constructor that only aims to init members and random numbers
            generator.
        """
        random.seed(time.time())

        self._ip_cache = []

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, type_exc, value, traceback):
        self.close()
        return False

    def open(self):
        """
            Open connection to Mongo and retrieve collection objects.
        """
        self._client = pymongo.MongoClient(
            'mongodb://{}:{}@{}:{}/{}'.format(
                settings.MONGODB['user'],
                settings.MONGODB['password'],
                settings.MONGODB['host'],
                settings.MONGODB['port'],
                settings.MONGODB['db']
            ),
            ssl=settings.MONGODB['secured']
        )

        self._db = self._client[settings.MONGODB['db']]
        self._check_collections_exists()

        self._ip_collection = self._db[IP_COLLECTION]

        self._raw_collection = self._db[RAW_COLLECTION]
        self._archive_collection = self._db[ARCHIVE_COLLECTION]
        self._spamhaus_collection = self._db[SPAMHAUS_COLLECTION]

    def _check_collections_exists(self):
        """
            Check whether required collections exist. If not, create missing ones.
        """
        existing_collections = self._db.collection_names()
        if IP_COLLECTION not in existing_collections:
            self._create_collection(IP_COLLECTION)

        if RAW_COLLECTION not in existing_collections:
            self._create_collection(RAW_COLLECTION)

        if ARCHIVE_COLLECTION not in existing_collections:
            self._create_collection(ARCHIVE_COLLECTION)

        if SPAMHAUS_COLLECTION not in existing_collections:
            self._create_collection(SPAMHAUS_COLLECTION)

    def _create_collection(self, name):
        """
            Create a single collection.

            :param str name: Name of the collection to create
        """
        LOGGER.info('Creating collection [%s]...', name)
        self._db.create_collection(name)

    def close(self):
        """ Close mongo's connection. """
        self._client.close()

    def push_ip_document(self, input_dict):
        """
            Push a new document regarding an IP or update existing document to
            append new data.

            :param dict input_dict: Expect a dictionnary having at least those
                fields: [IP, filename, weight, source, timestamp, raw]
        """
        file_doc = self._build_file_document(input_dict)
        input_dict['filename'] = file_doc['filename']

        if self.does_ip_exist(input_dict['ip']):
            LOGGER.debug('IP [%s] already exists. Update...', input_dict['ip'])
            self._ip_collection.update(
                {'ip': input_dict['ip']},
                {'$push': {'events': self._build_event_document(input_dict)}}
            )
        else:
            LOGGER.debug('Brand new IP [%s]. Insert...', input_dict['ip'])
            doc = self._build_full_document(input_dict)
            self._ip_collection.save(doc)
            self._ip_cache.append(input_dict['ip'])

        self._raw_collection.save(file_doc)

    def does_ip_exist(self, addr):
        """
            Check whether an IP address is known in the database.

            :param str addr: IP address to check
            :rtype: bool
            :return: `True` if IP address exists in the database, `False` otherwise
        """

        # To speed up these queries, a simple cache is maintained.
        if addr in self._ip_cache:
            return True

        res = self._ip_collection.find({'ip': addr}).count() > 0
        if res:
            self._ip_cache.append(addr)

        return res

    def _build_full_document(self, input_dict):
        """
            Build IP document to push into the collection.

            :param dict input_dict: Expect a dictionnary having at least those fields:
                [IP, filename, weight, source, timestamp]
            :rtype: dict
            :return: A dictionnary ready to be pushed in the mongo's collection.
        """
        return {
            'ip': input_dict['ip'],
            'events': [self._build_event_document(input_dict)]
        }

    def _build_event_document(self, input_dict):
        """
            Build sub-document that describe an event about IP reputation. This sub-document contains
            every details needed to understand what goes wrong with this IP.

            :param dict input_dict: Expect a dictionnary having at least those fields: [IP, filename, weight, source, timestamp]
            :rtype: dict
            :return: A dictionnary ready to be attached as an event.
        """
        return {
            'timestamp': input_dict['timestamp'],
            'source': input_dict['source'],
            'weight': input_dict['weight'],
            'filename': input_dict['filename']
        }

    def _build_file_document(self, input_dict):
        """
            Build file document to be pushed. These documents archive files generating an event.
            This might be the single RBL line or an entire FBL e-mail.

            :param dict input_dict: Expect a dictionnary having at least those fields:
                [IP, filename, weight, source, timestamp, raw]
            :rtype: dict
            :return: A dictionnary ready to be pushed into the file collection
        """
        current_ts = int(time.time() * 100)
        raw_hash = hashlib.sha256(input_dict['raw']).hexdigest()
        rnd_val = random.randint(10000, 99999)

        filename = '{}-{}-{}'.format(current_ts, raw_hash, rnd_val)

        return {
            'filename': filename,
            'data': input_dict['raw']
        }

    def purge_old_documents(self):
        """
            Archive IP sub-documents older than a month ago. These documents are moved
            into a dedicated archiving collection.
        """
        total_count = 0
        request = {
            'events.timestamp': {
                '$lt': A_MONTH_AGO
            }
        }

        LOGGER.debug("Archiving events older than %d...", A_MONTH_AGO)
        for doc in self._ip_collection.find(request):
            archives_bulk = []

            for event in doc['events']:
                # All documents having at least 1 timestamp < A_MONTH_AGO are retrieved.
                # This condition removes subdocuments that do not match.
                if event['timestamp'] < A_MONTH_AGO:
                    archives_bulk.append({
                        'ip': doc['ip'],
                        'filename': event['filename'],
                        'source': event['source'],
                        'weight': event['weight'],
                        'timestamp': event['timestamp']
                    })

            result = self._archive_collection.insert(archives_bulk)
            total_count = total_count + len(result)

        result = self._ip_collection.update(request, {
            '$pull': {
                'events': {
                    'timestamp': {
                        '$lt': A_MONTH_AGO
                    }
                }
            }
        }, multi=True)
        LOGGER.info('%d documents archived.', total_count)

        # Remove single entries
        result = self._ip_collection.remove({
            'events.timestamp': {
                '$exists': False
            }
        }, multi=True)

        LOGGER.info('%d single entries have been removed.', result['n'])

    def find_highest_scores(self):
        """
            Compute the top 10 of IP having the worst reputation by summing the weights
            of every events per IP.

            :rtype: cursor
            :return: A cursor pointing to sorted IP having the worst reputation.
        """
        collection = self._ip_collection.map_reduce(
            Code("function() {" +
                 "for(var i in this.events) {" +
                 "    emit(this.ip, this.events[i].weight);" +
                 "}" +
                 "}"),
            Code("function(k,v) {"
                 "return Array.sum(v)"
                 "}"),
            TOPTEN_COLLECTION
        )

        return collection.find().limit(TOP_LIMIT).sort('value', -1)

    def find_all_event_data_for_ip(self, addr, start_date=0, include_archives=False):
        """
            Retrieve IP events details and associated raw content involved in the event.

            :param str addr: IP address to find
            :param int start_date: Timestamp the events must be retrieved from
            :param bool include_archives: Do the results must also include archives?
            :rtype: array
            :return: An array containing every detailed event for passed IP.
        """
        results = []

        doc = self._ip_collection.find_one({'ip': addr})
        if doc:
            for entry in doc['events']:
                if entry['timestamp'] < start_date:
                    continue

                fdoc = self._raw_collection.find_one({'filename': entry['filename']})

                entry['data'] = fdoc['data']
                results.append(entry)

        if include_archives:
            archived_events = self._find_archived_events(addr, start_date)
            if archived_events:
                for entry in archived_events:
                    fdoc = self._raw_collection.find_one({'filename': entry['filename']})

                    entry['data'] = fdoc['data']
                    results.append(entry)

        return results

    def find_all_events_for_ip(self, addr, start_date=0, include_archives=False):
        """
            Retrieve all events (archived ones too) for an ip address and newer
            than `start_date`.

            :param str addr: IP address to find
            :param int start_date: Timestamp the events must be retrieved from
            :param bool include_archives: Do the results must also include archives?
            :rtype: array
            :return: An array containing all attached events.
        """
        if not start_date:
            start_date = utils.get_a_month_ago_date()

        doc = self._ip_collection.find_one({'ip': addr})
        if doc:
            events = [event for event in doc['events'] if event['timestamp'] >= start_date]
        else:
            events = []

        if include_archives:
            archived_events = self._find_archived_events(addr, start_date)
            events.extend(archived_events)

        return events

    def _find_archived_events(self, addr, start_date=0):
        """
            Find every archived documents for a given IP addr and newer than
            `start_date`.
        """
        events = []

        archives = self._archive_collection.find({'ip': addr, 'events.timestamp': {'$gte': start_date}})
        if archives:
            for event in archives:
                event.pop('ip')
                event.pop('_id')
                events.append(event)

        return events

    def update_spamhaus_entries(self, documents):
        """
            Update or insert an spamhaus entries into the spamhaus mongo collection. For each entry that
            is no longer active, update them to set their attr `active` to false.

            :param tuple document: Tuple of dictionnary representing documents to upsert having at least
            those mandatory keys: [sbl_number, cidr]
        """
        now = datetime.now()

        # First upsert still active entries
        for document in documents:
            query = {
                'sbl_number': document['sbl_number']
            }

            document['active'] = True
            document['last_seen'] = now
            self._spamhaus_collection.update(query, document, upsert=True)

        # Now, set inactive all active documents that are not in documents
        active_ids = [doc['sbl_number'] for doc in documents]
        query = {
            'sbl_number': {
                '$nin': active_ids
            },
            'active': True
        }

        res = self._spamhaus_collection.update(query, {'$set': {'active': False}}, multi=True)

    def find_spamhaus_entries(self, is_active=None):
        """
            Retrieve all registered spamhaus tickets.

            :param bool is_active: (Optional) Filter tickets depending if they're still active or not.
            :rtype: cursor
            :return: All desired spamhaus tickets sorted by first_seen date (asc)
        """
        query = {}
        if is_active is not None:
            query['active'] = is_active

        return self._spamhaus_collection.find(query).sort('first_seen', 1)
