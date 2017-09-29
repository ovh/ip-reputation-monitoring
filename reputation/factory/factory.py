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
    Factory module allowing users to inject their own implementation of our interface.
"""

import importlib
import inspect
from config import settings
from utils.logger import LOGGER


class WrongImplementationException(Exception):
    """
        Exception raised when provided implementation does not inherit of our interface.
    """
    pass


class ImplementationNotFoundException(Exception):
    """
        Exception raised when requested implementation has not been provided by user configuration.
    """
    pass


class ImplementationFactory(object):
    """
        This handy magical class provides an easy way to let users inject their own implementations of
        business/data access classes in the application by reading the configuration and instantiating
        the object at runtime.
    """

    def __init__(self):
        """
            Constructor: initialize adapter implementations
        """
        self._registered_implementations = {}
        self._registered_instances = {}

        self.__read_custom_implementations()

    def get_instance_of(self, string, *args):
        """
            Spawn a new instance of a class, passing to the constructor provided args.

            :param str string: Whished class instance identifier
            :param array args: Arguments to passed to the class constructor
            :return: A new instance of the requested class
            :raises ImplementationNotFoundException: No implementation match passed identifier
        """
        if string not in self._registered_implementations:
            raise ImplementationNotFoundException(string)

        return self._registered_implementations[string](*args)

    def get_singleton_of(self, string):
        """
            Still return the same instance of a given class.

            :param str string: Wished class instance identifier
            :return: The only instance of the requested class
            :raises ImplementationNotFoundException: No implementation match passed identifier
        """
        if string not in self._registered_instances:
            self._registered_instances[string] = self.get_instance_of(self, string)

        return self._registered_instances[string]

    def __read_custom_implementations(self):
        for impl in settings.CUSTOM_IMPLEMENTATIONS:
            class_object = self.__get_impl_adapter_from_string(impl)
            class_base = self.__get_base_adapter(class_object)
            # Ensure the implementation really implements provided interface
            if not class_base:
                raise WrongImplementationException(impl)

            self.__register_impl(class_base, class_object)

    def __get_impl_adapter_from_string(self, string):
        module_name, cls_name = string.rsplit('.', 1)
        return getattr(importlib.import_module(module_name), cls_name)

    def __get_base_adapter(self, class_obj):
        ancestors = inspect.getmro(class_obj)
        for cls in ancestors:
            if cls.__module__.startswith("adapters"):
                return cls

        return None

    def __register_impl(self, base, class_obj):
        self._registered_implementations[base.__name__] = class_obj

        LOGGER.debug("Custom implementation [%s] registered.", class_obj)


# Before instantiate the singleton, check it has not already been done.
if not hasattr(ImplementationFactory, 'instance'):
    ImplementationFactory.instance = ImplementationFactory()
