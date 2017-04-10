# -*- coding: utf-8 -*-
import unittest
import operator
import os
from tempfile import TemporaryFile

from core.tools.serialization import save_tree, load_tree


class SerializationTest(unittest.TestCase):

    def tearDown(self):
        if os.path.exists('test.json'):
            os.remove('test.json')

    def test_save_load_tree(self):
        """保存和读取树"""
        # TODO: 如何替换掉内建库的函数open， 变成TemporaryFile 来方便测试？
        open = lambda x: x
        tree = {
            'b': {'atime': 1},
            'b/': {'c': {'ctime': 2}}
        }
        save_tree('test.json', tree)
        rst = load_tree('test.json')
        self.assertEqual(rst, tree)
