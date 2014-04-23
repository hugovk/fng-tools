#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Unit tests for artists.py
"""
from __future__ import unicode_literals
import unittest
import artists


class TestIt(unittest.TestCase):

    def test_1(self):
        date = '1895-04-02'
        year = artists.year_from_date(date)
        self.assertEqual(year, 1895)

    def test_2(self):
        date = '1699'
        year = artists.year_from_date(date)
        self.assertEqual(year, 1699)

    def test_3(self):
        date = None
        year = artists.year_from_date(date)
        self.assertEqual(year, None)

    def test_4(self):
        date = "1741 (jälkeen)"
        year = artists.year_from_date(date)
        self.assertEqual(year, 1741)

    def test_5(self):
        date = "1700?"
        year = artists.year_from_date(date)
        self.assertEqual(year, 1700)

    def test_6(self):
        date = "(1500)"
        year = artists.year_from_date(date)
        self.assertEqual(year, 1500)

    def test_7(self):
        date = "n. 1630"
        year = artists.year_from_date(date)
        self.assertEqual(year, 1630)


if __name__ == '__main__':
    unittest.main()

# End of file
