#!/usr/bin/env python3

""" Default storage implementation unit tests """

import os
import unittest
from adapters.services.secrets import SecretsServiceException
from default.adapters.services.secrets import EnvironmentSecretService

SECRET_NAME = "A_SECRET"
SECRET_CONTENT = "Hello world !"


class TestDefaultSecretsImpl(unittest.TestCase):

    def tearDown(self):
        """ Cleanup environ """
        if SECRET_NAME in os.environ:
            del os.environ[SECRET_NAME]

    def test_read(self):
        """ Standard read that should succeed """
        os.environ[SECRET_NAME] = SECRET_CONTENT
        secrets = EnvironmentSecretService()

        buf = secrets.read(SECRET_NAME)
        self.assertEqual(SECRET_CONTENT, buf)

    def test_cannot_read(self):
        """ Secret does not exist => should raise a SecretsServiceException """
        with self.assertRaises(SecretsServiceException):
            secrets = EnvironmentSecretService()
            secrets.read(SECRET_NAME)
