#!/usr/bin/env python3
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
import factory.factory
import sys


def get_secret(secret_name):
    with factory.factory.ImplementationFactory.instance.get_singleton_of("SecretsServiceBase") as secrets:
        try:
            return secrets.read(secret_name)
        except:
            return ""


#: DB settings
MONGO_DB = {
    'host': get_secret('MONGO_HOST'),
    'port': get_secret('MONGO_PORT'),
    'db': get_secret('MONGO_DB'),
    'user': get_secret('MONGO_USER'),
    'password': get_secret('MONGO_PASSWORD'),
    'secured': True
}
SPAMHAUS_DB = {
    'host': get_secret('POSTGRES_HOST'),
    'port': get_secret('POSTGRES_PORT'),
    'db': get_secret('POSTGRES_DB'),
    'user': get_secret('POSTGRES_USER'),
    'password': get_secret('POSTGRES_PASSWORD'),
    'secured': True
}

#: Global Email settings (inbox creds, header and reporting)
SCORING_EMAIL = {
    'host': get_secret('EMAIL_HOST'),
    'reporting': {
        'from': get_secret('REPORTING_SENDER'),
        'to': get_secret('REPORTING_TARGET')
    },
    'polling': {
        'user': get_secret('FBL_USER'),
        'password': get_secret('FBL_PASSWORD')
    },
    'partner_header': get_secret('FBL_PARTNER_HEADER')
}

if __name__ == "__main__":
    secret = get_secret(sys.argv[1])
    if not secret:
        print("{} is empty: '{}'".format(sys.argv[1], secret), file=sys.stderr)
    print(secret)
