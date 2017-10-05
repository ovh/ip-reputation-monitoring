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

"""
    IP Reputation Monitoring observes RBL and FBL and maintains a hall of fame about
    IPs having the worst reputation.
"""

import os
import sys
from adapters.services import storage
from archive import archive
from db import mongo
from parsing.registered import parsers
from reporting import reporter


def usage(app):
    print("ip-reputation-monitoring - Copyright (c) 2016, OVH SAS.")
    print("This program comes with ABSOLUTELY NO WARRANTY.")
    print("This is free software, and you are welcome to redistribute it under certain conditions.")
    print("For more details, see <http://www.gnu.org/licenses/>.")
    print()
    print("Usage:")
    print("      " + app + " --parse [[--snds|--cleantalk|--blocklist|--stopforumspam] <file>|--mails]")
    print("      " + app + " --purge")
    print("      " + app + " --scores")
    sys.exit(1)


def get_parser_class(name):
    """
        From a parser name, return the class to instantiate

        :param str name: Name of the parser to instantiate
        :rtype: class
    """
    if name == 'mails':
        # Put AOL but it could be SignalSpam / SpamCop since it's the same parser.
        return parsers['AOL']

    for k in parsers.keys():
        if k.lower() == name:
            return parsers[k]

    return None


def run_parser(name, args=None):
    """
        Parse incoming data

        :param str name: Name of the parser to instantiate
        :param Object args: Optional arguments to pass to the parser
    """
    parser_class = get_parser_class(name)

    if not parser_class:
        raise Exception(str('Unavailable parser for [{}].'.format(name)))

    parser = parser_class(args) if args else parser_class()
    parser.run()
    sys.exit(0)


def purge_database():
    """
        Archive old documents
    """
    with mongo.Mongo() as database:
        database.purge_old_documents()
    sys.exit(0)


def send_score_report():
    """
        Send reports concerning the 10th ip having the worst reputation.
    """
    reporter.Reporter().send_reports()
    sys.exit(0)


def check_input_file(input_file):
    """
        Check input file exists and is not empty.

        :param str input_file: file to check
        :rtype: bool
        :return: `True` if file is ready to be parsed, `False` otherwise
    """
    if not os.path.exists(input_file):
        return False

    return os.stat(input_file).st_size > 0


def main(argv):
    """
        Reputation monitoring entry point
    """
    if len(argv) >= 3:
        if argv[1] == '--parse':
            input_type = argv[2].replace('--', '')
            if input_type in ('snds', 'cleantalk', 'blocklist', 'stopforumspam') and len(argv) == 4:
                if not check_input_file(argv[3]):
                    raise Exception('Input file is invalid (does it exist and has several lines?)')

                # First, try to archive. If it fails, dont go further.
                try:
                    archive.archive_rbl(argv[3], input_type)
                except storage.StorageServiceException:
                    raise Exception('Cannot parse file since it cannot be archived in Swift.')

                run_parser(input_type, argv[3])
                os.remove(argv[3])
            elif input_type == 'mails':
                run_parser(input_type)
    elif len(argv) == 2:
        if argv[1] == '--purge':
            purge_database()
        elif argv[1] == '--scores':
            send_score_report()

    usage(argv[0])
    sys.exit(1)


if __name__ == "__main__":
    main(sys.argv)
