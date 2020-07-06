#!/usr/bin/python3
""" test console
"""


import unittest
import sys
from console import HBNBdata
from unittest.mock import create_autospec


class TestConsole(unittest.TestCase):
    """ class testing console
    """
    def setUp(self):
        """ standard setUp """
        self.mock_stdin = create_autospec(sys.stdin)
        self.mock_stdout = create_autospec(sys.stdout)

    def create(self, server=None):
        """ create """
        return HBNBdata(stdin=self.mock_stdin, stdout=self.mock_stdout)

    def test_exit(self):
        """ test exit command """
        cli = self.create()
        self.assertTrue(cli.onecmd("quit"))
        self.assertTrue(cli.onecmd("EOF"))

    def _last_write(self, nr=None):
        """:return: last `n` output lines"""
        if nr is None:
            return self.mock_stdout.write.call_args[0][0]
        return "".join(map(lambda c: c[0][0],
                           self.mock_stdout.write.call_args_list[-nr:]))


if __name__ == "__main__":
    unittest.main()
