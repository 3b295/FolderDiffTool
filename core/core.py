# -*- coding: utf-8 -*-
import os
import time
import copy
from typing import Union
from hashlib import sha1

from .tools.serialization import load_dict, save_dict
from .tools.color_print import Green, Red, Black, Blue

STRFTIME_TEMP = '%Y-%m-%d %H:%M:%S'


class TreeNode(object):
    """Tree node"""

    # Todo: add __annotations__ for function
    def __init__(self, name=None, *args, **kwargs):
        self.attrs = {}
        self.name = name
        try:
            self.attrs['ctime'] = kwargs.get('ctime', None)
            self.attrs['atime'] = kwargs.get('atime', None)
            self.attrs['mtime'] = kwargs.get('mtime', None)
        except ValueError as e:
            pass

    def __eq__(self, other):
        if isinstance(other, self.__class__) and self.attrs == other.attrs and self.name == other.name:
            return True
        return False

    def __repr__(self):
        return "< {} name: {} {}>".format(self.__class__, self.name, self.__hash__())

    def __hash__(self):
        # 一个文件的全部属性相等（不包括名字）， 就认为他们相等
        return hash(frozenset(sorted(self.attrs.items())))


class FileNode(TreeNode):
    """File Node"""
    pass


class FolderNode(TreeNode):
    """Folder node"""

    def __init__(self, *args, **kwargs):
        super(FolderNode, self).__init__(*args, **kwargs)
        self._subnodes = set()

    def add_subnode(self, subnode):
        self._subnodes.add(subnode)

    def get_subnodes_amount(self):
        """返回子节点的数量"""
        return self._subnodes.__len__()

    def get_subnodes(self) -> set:
        """return subnodes of set form"""
        return self._subnodes

    # FIXME: folder属性相等和子节点属性相等应该分离成两个函数
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

    def __init__(self):
        self._tree = None

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
            rst = {'name': node.name, 'attrs': node.attrs}
            if isinstance(node, FolderNode):
                subnodes = [func(x) for x in node.get_subnodes()]
                rst.update({'subnodes': subnodes})

            return rst

        return func(self._tree)

    @staticmethod
    def dict2tree(_dict):
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

        return func(_dict)

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
            fs = os.listdir(_path)

            for f in fs:
                whole_f = os.path.join(_path, f)
                rst.add_subnode(self._create_help(whole_f))
        else:
            raise PathStrError('_path is {}'.format(_path))

        return rst

    def _get_date(self, folder: str) -> dict:
        """
        获取详细的文件信息
        
        :param folder: 获取信息的文件路径
        :return: 详细的文件信息
        """
        rst = {
            'ctime': time.strftime(STRFTIME_TEMP, time.localtime(os.path.getctime(folder))),
            'atime': time.strftime(STRFTIME_TEMP, time.localtime(os.path.getatime(folder))),
            'mtime': time.strftime(STRFTIME_TEMP, time.localtime(os.path.getmtime(folder))),
        }
        return rst

    def deff(self, other):
        """
        
        :param other: other tree deffed
        :return: None
        """

        def rec(former, latter):
            rst = former.__class__()

            if isinstance(rst, FolderNode):
                for i in set(latter.attrs.keys()) | set(former.attrs.keys()):
                    if i in ['mtime']:  # 文件夹记录mtime的话 页面有点乱
                        continue
                    rst.attrs[i] = DoalData(former.attrs.get(i, None), latter.attrs.get(i, None))

                ls = {x.name: x for x in latter.get_subnodes()}
                for sub in former.get_subnodes():
                    l = ls.pop(sub.name, None)
                    if l:
                        rst.add_subnode(rec(sub, l))
                    else:
                        rst.add_subnode(rec(sub, sub.__class__()))

                for v in ls.values():
                    rst.add_subnode(rec(v.__class__(), v))

            else:
                for i in set(latter.attrs.keys()) | set(former.attrs.keys()):
                    rst.attrs[i] = DoalData(former.attrs.get(i, None), latter.attrs.get(i, None))

            rst.name = DoalData(former.name, latter.name)

            return rst

        rst = DiffFileTree()
        rst._tree = rec(self._tree, other._tree)

        return rst

    def graph(self, ctime=False, atime=False, mtime=False):
        """ 图形化的树形结构 """

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
                    extra_data += "\t{}\t".format(subnode.attrs['ctime'])
                if atime:
                    extra_data += "\t{}\t".format(subnode.attrs['atime'])
                #  FIXME: 文件夹不想显示mtime属性， 先暂时屏蔽掉
                if mtime:
                    m = subnode.attrs['mtime']
                    if m:
                        extra_data += "\t{}\t".format(m)
                # from IPython import embed
                # embed()

                if indention[cur_level] > 1:
                    rst += '├── {}\t\t\t{}\n'.format(subnode.name, extra_data)
                elif indention[cur_level] == 1:
                    rst += '└── {}\t\t\t{}\n'.format(subnode.name, extra_data)

                if isinstance(subnode, FolderNode):
                    rst += get_tree(subnode, cur_level + 1)

                indention[cur_level] -= 1

            return rst

        return get_tree(self._tree, 0)

    def __repr__(self):
        return "<FileTree: folder in {}>".format(self._tree.name) if self._tree else "<FileTree: None>"


class DiffFileTree(FileTree):
    """表示两棵树diff的结果
    name   attrs中的数据全部被变成DoalDta类型的双重数据
    """
    pass


class DoalData(object):
    """同时储存新旧两个值"""
    NEW = 1
    CHANGE = 2
    DEL = 3
    NOCHANGE = 4

    def __init__(self, old, new):
        self.new = new
        self.old = old
        if new:
            if old:
                if new == old:
                    self.type = self.NOCHANGE
                else:
                    self.type = self.CHANGE
            else:
                self.type = self.NEW
        else:
            if old:
                self.type = self.DEL
            else:
                raise TypeError('old and new can not be None!')

    def __str__(self):
        if self.type == self.NEW:
            return Green(str(self.new))
        elif self.type == self.DEL:
            return Blue(str(self.old))
        elif self.type == self.CHANGE:
            return Red(str(self.old) + ' --> ' + str(self.new))
        elif self.type == self.NOCHANGE:
            return str(self.old)
        else:
            raise TypeError("<DoalData#type> is only [NEW, CHANGE, OLD]")

    def __getattr__(self, item):
        # FIXME: 子元素究竟用谁的子节点， 先暂时用原来的， 应该用两个子节点diff 过后的结果来做的
        if self.type == self.DEL:
            raise AttributeError("<DoalData> data is deleted")
        elif self.type == self.NEW:
            return getattr(self.new, item)
        elif self.type == self.CHANGE:
            return getattr(self.old, item)
        else:
            raise TypeError("<DoalData#type> is only [NEW, CHANGE, OLD]")


class PathStrError(Exception):
    """path string Error """
    pass
