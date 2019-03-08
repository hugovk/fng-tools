#!/usr/bin/env python3
"""
Unit tests for fng.py
"""
import unittest
import fng


class TestIt(unittest.TestCase):

    def test_1(self):
        text = 'leveys 40,00 cm'
        cm = fng.get_cm(text)
        self.assertEqual(cm, 40.0)

    def test_2(self):
        text = 'korkeus 41,50 cm'
        cm = fng.get_cm(text)
        self.assertEqual(cm, 41.5)

    def test_3(self):
        text = 'leveys p\xe4iv\xe4mitta 30,00 cm'
        cm = fng.get_cm(text)
        self.assertEqual(cm, 30.0)

    def test_4(self):
        text = "leveys 10,50 cm"
        cm = fng.get_cm(text)
        self.assertEqual(cm, 10.5)

    def test_5(self):
        text = "korkeus 7,50 cm"
        cm = fng.get_cm(text)
        self.assertEqual(cm, 7.5)

    def test_6(self):
        text = 'korkeus 72,50 cm'
        cm = fng.get_cm(text)
        self.assertEqual(cm, 72.5)

    def test_7(self):
        text = "korkeus, ovaali 5,50 cm"
        cm = fng.get_cm(text)
        self.assertEqual(cm, 5.5)

    def test_8(self):
        text = "koleveys 60,00 mm (Dimension unit)"
        cm = fng.get_cm(text)
        self.assertEqual(cm, 6.0)

    def test_9(self):
        text = "leveys 2.90 m"
        cm = fng.get_cm(text)
        self.assertEqual(cm, 290)

    def test_10(self):
        text = "korkeus 4.10 m"
        cm = fng.get_cm(text)
        self.assertEqual(cm, 410.0)

if __name__ == '__main__':
    unittest.main()