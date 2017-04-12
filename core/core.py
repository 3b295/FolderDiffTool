# -*- coding: utf-8 -*-
import os
import time
from typing import Union

from .tools.serialization import load_dict, save_dict

STRFTIME_TEMP = '%Y-%m-%d %H:%M:%S'


class TreeNode(object):
    """Tree node"""

    # Todo: add __annotations__ for function
    def __init__(self, name=None, *args, **kwargs):
        self.name = name
        try:
            self.ctime = kwargs.get('ctime', None)
            self.atime = kwargs.get('atime', None)
        except ValueError as e:
            pass

    def __eq__(self, other):
        if len(self.__dict__) != len(other.__dict__):
            return False

        if not isinstance(other, self.__class__):
            return False

        for k, v in self.__dict__.items():
            if any([lambda x: isinstance(t, x) for t in [str, int, float]]):
                if v != other.__dict__.get(k, None):
                    return False

        return True

    def __repr__(self):
        return "< {}'s object name: {} >".format(self.__class__, self.name)

    def __hash__(self):
        # FIXME: 这个hash只是能用， 我不知道是否是合适的写法
        return hash(''.join([k+str(v) for k, v in self.__dict__.items()]))


class FileNode(TreeNode):
    """File Node"""
    pass


class FolderNode(TreeNode):
    """Folder node"""

    def __init__(self, *args, **kwargs):
        super(FolderNode, self).__init__(*args, **kwargs)
        self._subnodes = []

    def add_subnode(self, subnode):
        self._subnodes.append(subnode)

    def get_subnodes_amount(self):
        """返回子节点的数量"""
        return self._subnodes.__len__()

    def get_subnodes(self) -> list:
        """return subnodes of list form"""
        return self._subnodes

    def __eq__(self, other):
        if not super(FolderNode, self).__eq__(other):
            return False
        if set(self._subnodes) == set(other._subnodes):
            return True
        return False

    def __hash__(self):
        return super(FolderNode, self).__hash__()


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

    @classmethod
    def from_json(cls, file):
        """使用一个JSON文件初始化树"""
        ex = cls.__new__(cls)
        ex._tree = FileTree.dict2tree(load_dict(file))
        return ex

    def save_json(self, folder):
        """保存为JSON格式的文件 """
        save_dict(folder, self.convert2dict())

    def convert2dict(self) -> dict:
        """将树转化为易于转化为dict的形式(尽量兼容JSON）
        
        :return: dict object
        """

        def func(node):
            rst = {key: value for key, value in node.__dict__.items()
                   if any([isinstance(value, x) for x in [str, float, int]])}
            if isinstance(node, FolderNode):
                subnodes = [func(x) for x in node.get_subnodes()]
                rst.update({'subnodes': subnodes})

            return rst

        return func(self._tree)

    @staticmethod
    def dict2tree(dict):
        """将 convert2dict 的过程反过来"""

        def func(node):
            f = None
            ls = []
            for k, v in node.items():
                if k == 'subnodes':
                    f = FolderNode()
                    for sub in v:
                        f.add_subnode(func(sub))
                else:
                    ls.append((k, v))

            if not f:
                f = FileNode()
            for k, v in ls:
                setattr(f, k, v)

            return f

        return func(dict)

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
            for subnode in tree.get_subnodes():

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
