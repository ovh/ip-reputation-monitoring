# -*- coding: utf-8 -*-
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
    DNSBL configuration.
"""

DNS_BL = (
    {'shortened': 'ACH', 'name': 'Abuse combined BL', 'uri': 'combined.abuse.ch'},
    {'shortened': 'SH', 'name': 'Spamhaus ZEN BL', 'uri': 'zen.spamhaus.org'},
    {'shortened': 'SCOP', 'name': 'Spamcop BL', 'uri': 'bl.spamcop.net'},
    {'shortened': 'AAT', 'name': 'Abuseat BL', 'uri': 'cbl.abuseat.org'},
    {'shortened': 'SORBS', 'name': 'Sorbs BL', 'uri': 'recent.spam.dnsbl.sorbs.net'},
    {'shortened': 'UCE', 'name': 'Uceprotect BL', 'uri': 'dnsbl-1.uceprotect.net'},
    {'shortened': 'MSRBL', 'name': 'Msrbl BL', 'uri': 'combined.rbl.msrbl.net'},
    {'shortened': 'WPBL', 'name': 'Wpbl BL', 'uri': 'db.wpbl.info'},
)
