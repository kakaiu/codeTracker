#!/usr/bin/python
# -*- coding: UTF-8 -*-
#__author__ :king-jojo

def list_all_node(dict_a):
    """Using recursive function to traverse the nodes and dump them into list"""
    node_list = []
    if isinstance(dict_a,dict):
        for x in range(len(dict_a)):
            temp_key = dict_a.keys()[x]
            temp_value = dict_a[temp_key]
            if isinstance(temp_value, list):
                for y in temp_value:
                    node_list.append(list_all_node(y))
            else:
                if temp_key == '_nodetype':
                    node_list.append(temp_value)
    return node_list

def Sequence_generate(node_list, num_list):

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
                sequence.append(node_list[0]['_nodetype'])
                seque_list.append(sequence)
                index_list.append(index)
    return [seque_list, index_list]

def Sequence_compare(seq1, seq2):
    list1 = []
    list2 = []
    for index1,str1 in enumerate(seq1):
        for index2,str2 in enumerate(seq2):
            if str1 == str2:
                list1.append(index1)
                list2.append(index2)
    return [is_arith_progression(list1,list2), list1, list2]

def is_arith_progression(index1, index2):
    s = False
    length = len(index1)
    if length > 1:
        for i in range(0, length-1):
            if index1[i+1] - index1[i] != 1:
                s = False
                break
            elif index2[i+1] - index2[i] != 1:
                s = False
                break
            else:
                s = True
    else:
        s = False
    return s

def Seqlist_compare(seq_list1, seq_list2):
    set1 = []
    set2 = []
    exit = []
    for index1,seq1 in enumerate(seq_list1[0]):
        for index2,seq2 in enumerate(seq_list2[0]):
            if Sequence_compare(seq1, seq2):
                if index2 not in exit:
                    set1 = list(set(set1).union(set(seq_list1[1][index1])))
                    set2 = list(set(set2).union(set(seq_list2[1][index2])))
                    exit.append(index2)
                    break
    return [set1, set2]


