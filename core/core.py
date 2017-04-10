# -*- coding: utf-8 -*-
import os
import time
from core.tools.serialization import load_tree, save_tree

STRFTIME_TEMP = '%Y-%m-%d %H:%M:%S'


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
        ex._tree = load_tree(file)
        return ex

    def save_json(self, filder):
        """保存为JSON格式的文件 """
        save_tree(filder, self._tree)

    def _create_help(self, folder: str) -> dict:
        """
        用于创建树形结构的迭代函数
        
        :param folder: 
        :return: 
        """
        rst = {}
        all = os.listdir(folder)
        for f in all:
            whole_f = os.path.join(folder, f)
            if os.path.isdir(whole_f):
                rst[f + '/'] = self._get_date(whole_f)
                rst[f + '/']['subdir'] = self._create_help(whole_f)
            elif os.path.isfile(whole_f):
                rst[f] = self._get_date(whole_f)

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

    def print(self, ctime=False):
        """
        图形化的树形结构

        """

        def get_tree(tree, cur_level, traces={}):
            """递归的打印tree"""
            rst = ''

            traces[cur_level] = len(tree)
            for key, value in tree.items():
                # FIXME: \n in linux
                for l in range(cur_level):
                    rst += '│   ' if traces[l] > 1 else '    '

                extra_data = ''
                #  添加额外的内容
                if ctime:
                    extra_data += time.strftime(STRFTIME_TEMP, time.localtime(value['ctime']))

                if traces[cur_level] > 1:
                    rst += '├── {}\t\t\t{}\n'.format(key, extra_data)
                elif traces[cur_level] == 1:
                    rst += '└── {}\t\t\t{}\n'.format(key, extra_data)

                if key.endswith('/'):
                    rst += get_tree(value['subdir'], cur_level + 1)

                traces[cur_level] -= 1

            return rst

        print(get_tree(self._tree, 0))

    def __str__(self):
        return "<FileTree {}>".format(self._tree)
