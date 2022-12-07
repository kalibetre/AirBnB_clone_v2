#!/usr/bin/python3
""" Module for testing db storage"""
import inspect
import unittest
from os import getenv

import MySQLdb
import pycodestyle

import console
from models.engine import db_storage

HBNBCommand = console.HBNBCommand
DBStorage = db_storage.DBStorage


class TestDBStorageDocsAndStyle(unittest.TestCase):
    """Tests DBStorage class for documentation and style conformance"""

    def test_pycodestyle(self):
        """Tests compliance with pycodestyle"""
        style = pycodestyle.StyleGuide(quiet=False)
        result = style.check_files(
            [
                "models/engine/db_storage.py",
                "tests/test_models/test_engine/test_db_storage.py"
            ])
        self.assertEqual(result.total_errors, 0)

    def test_module_docstring(self):
        """Tests whether the module is documented"""
        self.assertTrue(len(db_storage.__doc__) >= 1)

    def test_class_docstring(self):
        """Tests whether the class is documented"""
        self.assertTrue(len(DBStorage.__doc__) >= 1)

    def test_methods_docstring(self):
        """Tests whether the class methods are documented"""
        funcs = inspect.getmembers(DBStorage, inspect.isfunction)
        for func in funcs:
            self.assertTrue(len(func[1].__doc__) >= 1)

    def test_class_name(self):
        """Test whether the class name is correct"""
        self.assertEqual(DBStorage.__name__, "DBStorage")


@unittest.skipIf(getenv("HBNB_TYPE_STORAGE") != 'db', 'DBStorage Not In Use')
class TestDBStorage(unittest.TestCase):
    """Test cases for DBStorage Class"""

    @classmethod
    def setUpClass(cls):
        """initial configuration for tests"""
        cls.conn = MySQLdb.connect(
            host=getenv("HBNB_MYSQL_HOST"),
            port=3306,
            user=getenv("HBNB_MYSQL_USER"),
            passwd=getenv("HBNB_MYSQL_PWD"),
            db=getenv("HBNB_MYSQL_DB"),
            charset="utf8"
        )
        cls.cur = cls.conn.cursor()
        cls.storage = DBStorage()
        cls.storage.reload()
        cls.cmd = HBNBCommand()

    @classmethod
    def tearDownClass(cls):
        """cleanup test files"""
        cls.cur.close()
        cls.conn.close()
        del cls.cmd

    def test_save_method_with_state(self):
        """tests if the DB stores a state object"""
        self.cur.execute("SELECT * FROM states")
        exp_len = len(self.cur.fetchall())
        self.cmd.onecmd('create State name="California"')
        self.cur.execute("SELECT * FROM states")
        self.assertEqual(len(self.cur.fetchall()), exp_len + 1)
