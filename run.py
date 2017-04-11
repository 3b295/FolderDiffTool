# -*- coding: utf-8 -*-
from core import FileTree


if __name__ == '__main__':
    ft = FileTree.from_folder('.')
    print(ft.graph(ctime=True))
