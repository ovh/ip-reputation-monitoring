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
    Archive parsed RBL files.
"""

import os
import time
from config import settings
from factory.factory import ImplementationFactory


def archive_rbl(filename, rbl_type):
    """
        Store RBL in using the :py:class:`adapters.services.storage.StorageServiceBase`
        implementation.

        :param str filename: Path of the file to archive
        :param str rbl_type: RBL name the file refers to
        :rtype: bool
        :return: `True` if everything went ok, `False` otherwise
    """
    suffix = time.strftime('%y%m%d-%H%M%S')

    object_name = '.'.join([
        os.path.join(rbl_type, os.path.basename(filename)),
        suffix
    ])

    with open(filename, 'rb') as fdesc:
        with ImplementationFactory.instance.get_instance_of("StorageServiceBase", settings.RBL_STORAGE_CONTEXT) as storage:
            return storage.write(object_name, fdesc.read())
