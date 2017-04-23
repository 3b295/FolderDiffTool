# -*- coding: utf-8 -*-
import unittest
import os
from tempfile import mkdtemp
from core import FileTree
from core.core import FileNode, TreeNode, FolderNode
from core.tools.serialization import save_dict
import shutil


class FileTreeTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(FileTreeTest, self).__init__(*args, **kwargs)
        self._tmp = mkdtemp()
        for pa in map(lambda x: os.path.normcase(os.path.join(self._tmp, x)),
                      ['a/a2/a3', 'b/a/a', 'b/a/b', 'b/KJDSFKLkdjf8234lsf']):
            os.makedirs(pa)
        with open(os.path.join(self._tmp, 'b/a/a/test.txt'), 'ab') as f:
            f.write(b'this is DataDiffManger unittest temp file')
            f.write(b'[github]("https://github.com/3b295/FolderDiffTool")')

    def __del__(self):
        shutil.rmtree(self._tmp)

    def test_from_folder(self):
        ft = FileTree.from_folder(self._tmp)
        self.assertEquals({x.name for x in ft._tree.get_subnodes()}, {'a', 'b'})
        with open(os.path.join(self._tmp, 'b/a/a/test.txt'), 'rb') as f:
            self.assertIn(b'unittest', f.read())

    def test_form_json(self):
        ft = FileTree.from_folder(self._tmp)
        jsonfile = os.path.join(self._tmp, 'test.json')
        ft.save_json(jsonfile)
        ft2 = FileTree.from_json(jsonfile)

        self.assertEquals(ft._tree, ft2._tree)

    def test_print(self):
        ft = FileTree.from_folder(self._tmp)
        self.assertIn('KJDSFKLkdjf8234lsf'.lower(), ft.graph())
        self.assertIn('KJDSFKLkdjf8234lsf'.lower(), ft.graph(ctime=True))

    def test_conver2dict_and_dict2tree(self):
        ft = FileTree.from_folder(self._tmp)
        dic = ft.convert2dict()
        self.assertEquals(set([x['name'] for x in dic['subnodes']]),
                          {'a', 'b'})

        self.assertEquals(ft._tree, ft.dict2tree(dic))


class TreeNodeTest(unittest.TestCase):
    def test_eq(self):
        f = TreeNode()
        f2 = TreeNode()
        self.assertEquals(f, f2)

        f.atime = 'test atime'
        f.ctime = 'test ctime'
        f2.atime = 'test atime'
        f2.ctime = 'test ctime'
        self.assertEquals(f, f2)

    def test_eq_not(self):
        f = TreeNode()
        f2 = TreeNode()

        f.attrs['atime'] = 'test atime'
        self.assertNotEquals(f, f2)
        f2.attrs['atime'] = 'not atime'
        self.assertNotEquals(f, f2)
        f.attrs['ctime'] = 'test ctime'
        self.assertNotEquals(f, f2)
        f2.attrs['xxx'] = 'xxx'
        self.assertNotEquals(f, f2)


class FolderNodeTest(unittest.TestCase):
    def test_eq_folder_msg(self):
        # 文件夹信息不同
        fd = FolderNode('test')
        fd2 = FolderNode('test')
        self.assertEquals(fd, fd2)

        fd = FolderNode('test')
        fd2 = FolderNode('fff')
        self.assertNotEquals(fd, fd2)

    def test_eq_subfolder(self):
        # 子文件夹
        fd = FolderNode('test')
        fd2 = FolderNode('test')
        sfd = FolderNode('sub')

        fd.add_subnode(sfd)
        self.assertNotEquals(fd, fd2)
        fd2.add_subnode(FolderNode('sub'))
        self.assertEquals(fd, fd2)
        sfd.add_subnode(FileNode('subfile'))
        self.assertNotEquals(fd, fd2)

    def test_eq_subfile(self):
        # 子文件
        fd = FolderNode('test')
        fd2 = FolderNode('test')

        fd.add_subnode(FileNode('filenode'))
        fd2.add_subnode(FileNode('filenode'))
        self.assertEquals(fd, fd2)

        fd.add_subnode(FileNode('filenode'))
        fd2.add_subnode(FileNode('xxxxxx'))
        self.assertNotEquals(fd, fd2)
