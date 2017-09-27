#!/usr/bin/env python3
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

"""
Monitoring of IP reputations using various FBL/RBL.
"""
from pip.req import parse_requirements
from setuptools import setup, find_packages


def get_requirements():
    reqs = parse_requirements('requirements.txt')
    return [str(current.req) for current in reqs]


setup(
    name='ip-reputation-monitoring',
    version='1.1.0',
    description="A toolset allowing anyone to monitor given IPs reputation over the Internet.",
    url='https://www.ovh.com/',
    license='BSD',
    author='OVH',
    author_email='sebastien.meriot@corp.ovh.com',
    install_requires=get_requirements(),
    packages=find_packages(exclude=['tests']),
    test_suite='tests',
)
