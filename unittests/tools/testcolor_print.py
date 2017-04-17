# -*- coding: utf-8 -*-

from core.tools.color_print import Red
import unittest


class TestCmdColor(unittest.TestCase):
    def test_C(self):
        self.assertIn('x', Red('x'))
        self.assertNotIn('x', Red('n'))
        self.assertIn('\033[0;0m', Red('x'))
        self.assertIn('\033[31m', Red('x'))


