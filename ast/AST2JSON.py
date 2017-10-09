#!/usr/bin/python
# -*- coding: UTF-8 -*-

__author__  = 'king-jojo'

import json
import re

RE_AZ = re.compile(r'-(.*?) ')

def to_dict(node_list):
    """Transform the node list into nested dictionary"""
    node_list_cp = node_list[:]
    cp_list = []
    AST_dict = dict()
    AST_dict['_nodetype'] = node_list_cp[0]['_nodetype']
    AST_dict['coord'] = node_list_cp[0]['coord']
    first_sublist = []
    for x in range(1, len(node_list_cp)):
        num = node_list_cp[x]['_nodetype'].find('-')
        cp_list.append(num)
        cut = re.findall(RE_AZ, node_list_cp[x]['_nodetype'])
        if len(cut) > 0:
            node_list_cp[x]['_nodetype'] = cut[0]
        else:
            node_list_cp[x]['_nodetype'] = ''
    num_list = cp_list[:]
    for y in range(max(num_list) - 2, 0, -2):
        for x in range(len(num_list) - 1, -1, -1):
            if num_list[x] == y:
                subnode_list = []
                for z in range(len(num_list) - 1, x - 1, -1):
                    if num_list[z] == y + 2:
                        subnode_list.append(node_list_cp[z + 1])
                        num_list[z] = 0
                node_list_cp[x + 1]['_subnode'] = subnode_list

    for x in range(0, len(num_list)):
        if num_list[x] == 1:
            first_sublist.append(node_list_cp[x + 1])

    AST_dict['_subnode'] = first_sublist
    return [AST_dict, cp_list, node_list]

def to_json(node_list, json_name):
    """Write into json format"""
    node_list_new = node_list[:]
    AST_dict = to_dict(node_list_new)
    with open(json_name, 'w+') as f:
        json.dump(AST_dict[0], f, ensure_ascii=False, indent=4)
    f.close()
