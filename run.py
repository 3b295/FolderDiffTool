# -*- coding: utf-8 -*-
from core import FileTree


if __name__ == '__main__':
    ft = FileTree.from_folder('.')
    ft.print(ctime=True)
