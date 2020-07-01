#!/usr/bin/python3
"""
Unittest for the consolefile
"""


import unittest
import sys
import os
from io import StringIO
from unittest.mock import create_autospec
from console import HBNBCommand
from models import storage


class TestConsole(unittest.TestCase):
    """ Test console.py
    """
    def setUp(self):
        """ setup
        """
        self.mock_stdin = create_autospec(sys.stdin)
        self.mock_stdout = create_autospec(sys.stdout)
        self.cli = self.create()
        sys.stdout = StringIO()
        if os.path.isfile("file.json"):
            os.remove("file.json")

    def tearDown(self):
        """ Tear
        """
        sys.stdout = sys.__stdout__
        if os.path.isfile("file.json"):
            os.remove("file.json")

    def create(self, server=None):
        """ create
        """
        return HBNBCommand(stdin=self.mock_stdin, stdout=self.mock_stdout)

    def test_quit(self):
        """ Test for quit
        """
        self.assertTrue(self.cli.onecmd("quit"))
        self.assertTrue(self.cli.onecmd("EOF"))

    def test_help(self):
        """ Test for help
        """
        self.cli.onecmd("help help")
        string = "List available commands with \"help\" or detailed help with "
        string += "\"help cmd\".\n"
        self.cli.onecmd("help create")

    def test_create(self):
        """ Test for create class
        """
        self.cli.onecmd("create User")
        self.assertTrue(sys.stdout.getvalue())
        self.flush_buffer()
        self.cli.onecmd("create")
        self.assertEqual("** class name missing **\n", sys.stdout.getvalue())
        self.flush_buffer()
        self.cli.onecmd("create MyModel")
        self.assertEqual("** class doesn't exist **\n", sys.stdout.getvalue())

    def test_destroy(self):
        """ Test for destroy class
        """
        self.cli.onecmd("destroy")
        self.assertEqual("** class name missing **\n", sys.stdout.getvalue())
        self.flush_buffer()
        self.cli.onecmd("destroy MyModel")
        self.flush_buffer()
        self.cli.onecmd("destroy BaseModel")
        self.flush_buffer()
        self.cli.onecmd("destroy BaseModel 123")
        self.flush_buffer()

    def test_update(self):
        """ Test for update class
        """
        self.cli.onecmd("update")
        self.assertEqual("** class name missing **\n", sys.stdout.getvalue())
        self.flush_buffer()
        self.cli.onecmd("update MyModel")
        self.assertEqual("** class doesn't exist **\n", sys.stdout.getvalue())
        self.flush_buffer()
        self.cli.onecmd("update BaseModel")
        self.assertEqual("** instance id missing **\n", sys.stdout.getvalue())
        self.flush_buffer()
        self.cli.onecmd("update BaseModel 123")
        self.assertEqual(
                "** attribute name missing **\n",
                sys.stdout.getvalue())
        self.flush_buffer()
        obj_dict = storage.all()

    def test_count_adv(self):
        """ Test count
        """
        obj_dict = storage.all()
        count = 0
        for k, v in obj_dict.items():
            if obj_dict[k].__class__.__name__ == "User":
                count += 1
        self.cli.onecmd("User.count()")
        self.assertEqual(str(count) + "\n", sys.stdout.getvalue())

    @staticmethod
    def flush_buffer():
        """ Flush buffer
        """
        sys.stdout.seek(0)
        sys.stdout.truncate(0)


if __name__ == '__main__':
    unittest.main()
