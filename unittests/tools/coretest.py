# -*- coding: utf-8 -*-
import unittest
import os
from core import FileTree
from core.tools.serialization import save_tree


class FileTreeTest(unittest.TestCase):
    def setUp(self):
        self.test_tree = {
            'b': {'atime': 1},
            'b/': {'c': {'ctime': 2}}
        }
        save_tree('test.json', self.test_tree)

    def tearDown(self):
        if os.path.exists('test.json'):
            os.remove('test.json')

    def test_from_folder(self):
        ft = FileTree.from_folder('E:/school_work')

    def test_from_json(self):
        ft = FileTree.from_json('test.json')
        self.assertEqual(ft._tree, self.test_tree)

    def test_save_json(self):
        ft = FileTree.from_json('test.json')
        ft.save_json('test2.json')
        with open('test.json', 'rb') as f1:
            with open('test2.json', 'rb') as f2:
                self.assertEqual(f1.read(), f2.read())

        if os.path.exists('test2.json'):
            os.remove('test2.json')

