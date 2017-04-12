# -*- coding: utf-8 -*-
import json


def load_dict(file):
    with open(file, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_dict(file, data):
    with open(file, 'w', encoding='utf-8') as f:
        json.dump(data, f)









