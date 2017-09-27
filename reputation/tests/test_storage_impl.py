#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Default storage implementation unit tests """

import os
import unittest
from adapters.services.storage import StorageServiceException
from default.adapters.services.storage import FilesystemStorageService

ROOT_STORAGE_DIR = "storage_test"
WRITTEN_FILE = "foo/bar.file"
FILE_CONTENT = b"Hello world !"


class TestDefaultStorageImpl(unittest.TestCase):

    def tearDown(self):
        """ Cleanup files & directories """
        complete_file_path = os.path.join(ROOT_STORAGE_DIR, WRITTEN_FILE)
        if os.path.exists(complete_file_path):
            os.remove(complete_file_path)

        if os.path.exists(ROOT_STORAGE_DIR):
            full_path_to_delete = os.path.join(ROOT_STORAGE_DIR, os.path.dirname(WRITTEN_FILE))
            if os.path.exists(full_path_to_delete):
                os.removedirs(full_path_to_delete)
            else:
                os.removedirs(ROOT_STORAGE_DIR)

    def test_read_write_delete(self):
        """ Standard read / write /delete sequence that should succeed """
        storage = FilesystemStorageService(ROOT_STORAGE_DIR)
        self.assertTrue(os.path.exists(ROOT_STORAGE_DIR))

        storage.write(WRITTEN_FILE, FILE_CONTENT)
        full_file_path = os.path.join(ROOT_STORAGE_DIR, WRITTEN_FILE)
        self.assertTrue(os.path.exists(full_file_path))

        buf = storage.read(WRITTEN_FILE)
        self.assertEqual(FILE_CONTENT, buf)

        storage.delete(WRITTEN_FILE)
        self.assertFalse(os.path.exists(full_file_path))

    def test_cannot_read(self):
        """ File does not exist => should raise a StorageServiceException """
        with self.assertRaises(StorageServiceException):
            storage = FilesystemStorageService(ROOT_STORAGE_DIR)
            storage.read(WRITTEN_FILE)

    def test_cannot_write(self):
        """ Cannot write in /bin (dont run this test as root please !) ==> StorageServiceException """
        with self.assertRaises(StorageServiceException):
            storage = FilesystemStorageService("/bin")
            storage.write("foo", b"bar")

    def test_cannot_delete(self):
        """ Try to delete a file that does not exist => StorageServiceException """
        with self.assertRaises(StorageServiceException):
            storage = FilesystemStorageService(ROOT_STORAGE_DIR)
            storage.delete(WRITTEN_FILE)
