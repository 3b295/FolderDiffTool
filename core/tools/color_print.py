# -*- coding: utf-8 -*-

__all__ = [
    'Default',
    'Black',
    'Red',
    'Green',
    'Yellow',
    'Blue',
    'Magenta',
    'Cyan',
    'White',
    'Bold',
    'Reverse',
    'Blackbg',
    'Redbg',
    'Greenbg',
    'Yellowbg',
    'Bluebg',
    'Magentabg',
    'Cyanbg',
    'Whitebg',
]

Reset = '\033[0;0m'


def Default(test):
    return '\033[0m' + test + Reset


def Black(test):
    return '\033[30m' + test + Reset


def Red(test):
    return '\033[31m' + test + Reset


def Green(test):
    return '\033[32m' + test + Reset


def Yellow(test):
    return '\03333m' + test + Reset


def Blue(test):
    return '\033[34m' + test + Reset


def Magenta(test):
    return '\033[35m' + test + Reset


def Cyan(test):
    return '\033[36m' + test + Reset


def White(test):
    return '\033[37m' + test + Reset


def Bold(test):
    return '\033[1m' + test + Reset


def Reverse(test):
    return '\033[2m' + test + Reset


def Blackbg(test):
    return '\033[40m' + test + Reset


def Redbg(test):
    return '\033[41m' + test + Reset


def Greenbg(test):
    return '\033[42m' + test + Reset


def Yellowbg(test):
    return '\033[43m' + test + Reset


def Bluebg(test):
    return '\033[44m' + test + Reset


def Magentabg(test):
    return '\033[45m' + test + Reset


def Cyanbg(test):
    return '\033[46m' + test + Reset


def Whitebg(test):
    return '\033[47m' + test + Reset



