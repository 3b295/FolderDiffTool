# -*- coding: utf-8 -*-
import unittest
import os
from tempfile import mkdtemp
from core import FileTree
from core.tools.serialization import save_tree


class FileTreeTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(FileTreeTest, self).__init__(*args, **kwargs)
        self._temp = mkdtemp()

        self.test_tree = {
            'b': {'atime': 1},
            'bf': {'c': {'ctime': 2}}
        }
        self.test_json_file = os.path.join(self._temp, 'test.json')

        for pa in map(lambda x: os.path.normcase(os.path.join(self._temp, x)),
                      ['a/a2/a3', 'b/a/a', 'b/a/a/KJDSFKLkdjf8234lsf']):
            os.makedirs(pa)

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_from_folder(self):
        ft = FileTree.from_folder(self._temp)

    def test_print(self):
        ft = FileTree.from_folder(self._temp)
        self.assertIn('KJDSFKLkdjf8234lsf'.lower(), ft.graph())
        self.assertIn('KJDSFKLkdjf8234lsf'.lower(), ft.graph(ctime=True))

