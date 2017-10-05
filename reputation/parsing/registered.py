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
    Module that auto-register detected parsers.
"""

import inspect
import pkgutil
from parsing import mails, csv


def _compute_parser_list():
    """
        Automatically recognize which parsers are available.

        :rtype: hash, hash
        :return: The first hash is of the form `{<parser_name1>: <parser_class1>}`.
            For each parser is associated its class. The second hash allows to
            shortened parser names (usefull for API) and has the folowwing form:
            `{<parser_name1>: <shortened_name1>}`.
    """
    parsers = {}
    shortened = {}

    # Browse both modules csv & mails
    for current in [csv, mails]:
        for importer, modname, ispkg in pkgutil.iter_modules(current.__path__):
            if ispkg:
                continue

            module = importer.find_module(modname).load_module(modname)
            members = inspect.getmembers(module, inspect.isclass)
            for member in members:
                # Hash is built using static method "get_description"
                if not hasattr(member[1], 'get_description'):
                    continue

                desc = member[1].get_description()

                if isinstance(desc, list):
                    for current in desc:
                        parsers[current['name']] = member[1]
                        shortened[current['name']] = \
                            current['name'] if 'shortened' not in current.keys() \
                            else current['shortened']
                else:
                    parsers[desc['name']] = member[1]
                    shortened[desc['name']] = desc['name'] if 'shortened' not in desc.keys() else desc['shortened']

    return parsers, shortened


parsers, shortened_names = _compute_parser_list()
