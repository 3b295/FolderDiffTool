# -*- coding: utf-8 -*-
from core import FileTree


if __name__ == '__main__':

    # ft = FileTree.from_folder(r'C:\Users\xwyst\Desktop\~DataDiffManger\a\test')
    # ft.save_json(r'C:\Users\xwyst\Desktop\~DataDiffManger\a\test\save.json')

    ft = FileTree.from_folder(r'C:\Users\xwyst\Desktop\~DataDiffManger\a\test')
    ft2 = FileTree.from_json(r'C:\Users\xwyst\Desktop\~DataDiffManger\a\test\save.json')
    fd = ft2.deff(ft)

    print(fd.graph(mtime=True))




