# -*- coding: utf-8 -*-
import os
import time
from typing import Union

from core.tools.serialization import load_tree, save_tree

STRFTIME_TEMP = '%Y-%m-%d %H:%M:%S'


class TreeNode(object):
    """Tree node"""

    # Todo: add __annotations__ for function
    def __init__(self, name, *args, **kwargs):
        self.name = name
        try:
            self.ctime = kwargs.get('ctime', None)
            self.atime = kwargs.get('atime', None)
        except ValueError as e:
            pass


class FileNode(TreeNode):
    """File Node"""
    pass


class FolderNode(TreeNode):
    """Folder node"""

    def __init__(self, *args, **kwargs):
        super(FolderNode, self).__init__(*args, **kwargs)
        self.subnodes = []

    def add_subnode(self, subnode):
        self.subnodes.append(subnode)

    def get_subnodes_amount(self):
        """返回子节点的数量"""
        return self.subnodes.__len__()


class FileTree(object):
    """文件树"""

    @classmethod
    def from_folder(cls, folder):
        """使用一个文件夹路径来初始化这棵树
        
        :param folder: 文件夹路径
        :return: None
        """
        ex = cls.__new__(cls)
        ex._tree = ex._create_help(folder)
        return ex

    def _create_help(self, _path: str) -> Union[FileNode, FolderNode]:
        """
        用于创建树形结构的迭代函数
        
        :param _path: 
        :return: 
        """
        if os.path.isfile(_path):
            filename = os.path.split(_path)[1]
            rst = FileNode(filename, **self._get_date(_path))
        elif os.path.isdir(_path):
            foldername = _path.split('\\')[-1]
            rst = FolderNode(foldername, **self._get_date(_path))
            all = os.listdir(_path)

            for f in all:
                whole_f = os.path.join(_path, f)
                rst.add_subnode(self._create_help(whole_f))
        else:
            raise Exception()

        return rst

    def _get_date(self, folder: str) -> dict:
        """
        获取详细的文件信息
        
        :param folder: 获取信息的文件路径
        :return: 详细的文件信息
        """
        rst = {
            'ctime': os.path.getctime(folder),
            'atime': os.path.getatime(folder),
        }
        return rst

    def deff(self, other):
        """
        
        :param other: other tree deffed
        :return: None
        """
        pass

    def graph(self, ctime=False):
        """
        图形化的树形结构
        """

        def get_tree(tree, cur_level, indention={}):
            """递归的打印tree"""
            rst = ''

            indention[cur_level] = tree.get_subnodes_amount()
            for subnode in tree.subnodes:
                subnode.name = subnode.name
                subnode = subnode

                # FIXME: \n in linux
                for l in range(cur_level):
                    rst += '│   ' if indention[l] > 1 else '    '

                extra_data = ''
                #  添加额外的内容
                if ctime:
                    extra_data += time.strftime(STRFTIME_TEMP, time.localtime(subnode.ctime))

                if indention[cur_level] > 1:
                    rst += '├── {}\t\t\t{}\n'.format(subnode.name, extra_data)
                elif indention[cur_level] == 1:
                    rst += '└── {}\t\t\t{}\n'.format(subnode.name, extra_data)

                if isinstance(subnode, FolderNode):
                    rst += get_tree(subnode, cur_level + 1)

                indention[cur_level] -= 1

            return rst

        return get_tree(self._tree, 0)

    def __str__(self):
        return "<FileTree {}>".format(self._tree)
