#!/usr/bin/python
# -*- coding: UTF-8 -*-

__author__  = 'king-jojo'

import json
import re

RE_AZ = re.compile(r'-(.*?) ')

def Sequence_gene(node_list, num_list):
    """From the root to the leaves, we traverse the tree to get all the sequences"""
    seque_list = []
    index_list = []
    for y in range(max(num_list), 1, -2):
        for x in range(len(num_list)-1, -1, -1):
            if num_list[x] == y:
                sequence = []
                index = []
                sequence.append(node_list[x + 1]['_nodetype'])
                index.append(x+1)
                for z in range(y-2, 0, -2):
                    for i in range(x-1, -1, -1):
                        if num_list[i] == z:
                            sequence.append(node_list[i + 1]['_nodetype'])
                            index.append(i+1)
                            break
                index.append(0)
                sequence.append(node_list[0]['_nodetype'])
                seque_list.append(sequence)
                index_list.append(index)
    return [seque_list, index_list]

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
    node_list_cp2 = node_list_cp[:]
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

    seq = Sequence_gene(node_list, cp_list)
    seque_list = seq[0]
    index_list = seq[1]
    count_dict = dict()
    trace_list = []
    for i in range(len(seque_list)):
        for k in range(len(index_list[i])):
            num = index_list[i][k]
            if count_dict.has_key(str(num)):
                continue
            else:
                count_dict[str(num)] = 'True'
                trace_dict = dict()
                trace_dict['id'] = num
                trace_dict['_nodetype'] = node_list_cp[num]['_nodetype']
                trace_dict['coord'] = node_list_cp[num]['coord']
                short_list = []
                for p in range(k, len(index_list[i]), 1):
                    short_list.append(index_list[i][p])
                trace_dict['trace'] = short_list
                trace_list.append(trace_dict)
            if len(count_dict) == len(node_list):
                break
    return [AST_dict, cp_list, node_list, trace_list]

def to_json(node_list, json_name1, json_name2, Tri=False):
    """Write into json format"""
    if Tri:
        node_list_new = node_list[:]
        final_list1 = []
        final_list2 = []
        for i in node_list_new:
            name = i[0]
            del i[0]
            AST_dict = to_dict(i)
            new_dict = dict()
            new_dict['__filename'] = name
            new_dict['__content'] = AST_dict[0]
            trace_newdict = dict()
            trace_newdict['__filename'] = name
            trace_newdict['__content'] = AST_dict[3]
            final_list1.append(new_dict)
            final_list2.append(trace_newdict)
        with open(json_name1, 'w+') as f1:
            json.dump(final_list1, f1, ensure_ascii=False, indent=4)
        f1.close()
        with open(json_name2, 'w+') as f2:
            json.dump(final_list2, f2, ensure_ascii=False, indent=4)
        f2.close()
    else:
        node_list_new = node_list[:]
        AST_dict = to_dict(node_list_new)
        with open(json_name1, 'w+') as f1:
            json.dump(AST_dict[0], f1, ensure_ascii=False, indent=4)
        f1.close()
        with open(json_name2, 'w+') as f2:
            json.dump(AST_dict[3], f2, ensure_ascii=False, indent=4)
        f2.close()
