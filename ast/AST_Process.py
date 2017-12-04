#!/usr/bin/python
# -*- coding: UTF-8 -*-

__author__  = 'king-jojo'

import os
import re

RE_NODE = re.compile(r'(.*?)0x')
RE_LINE = re.compile(r'<(\w.*?)>')


def AST_preprocess(code_path):
    """Preprocess of the code. Remove the head files and standard libraries"""
    path_new = './example/test_new.c'
    with open(code_path , 'r') as f:
        lines = f.readlines()
    f.close()

    with open(path_new , 'w') as f_new:
        for line in lines:
            if '#include' in line:
                line = '\n'
            f_new.write(line)
    f_new.close()
    return path_new

def AST_generate(code_path, preprocess):
    """Print AST based on command line"""
    if preprocess == True:
        code_path = AST_preprocess(code_path)
        # command = 'clang-check -ast-dump ' + code_path + ' --extra-arg="-ferror-limit=1" --extra-arg="-fno-color-diagnostics" --'
        command = 'clang-check -ast-dump ' + code_path + ' --extra-arg="-fno-color-diagnostics" --'
        F = os.popen(command)
        # (status, output) = commands.getstatusoutput('clang -Xclang -ast-dump -fsyntax-only ' + code_path)
    else:
        # command = 'clang-check -ast-dump ' + code_path + ' --extra-arg="-ferror-limit=1" --extra-arg="-fno-color-diagnostics" --'
        command = 'clang-check -ast-dump ' + code_path + ' --extra-arg="-fno-color-diagnostics" --'
        F = os.popen(command)
        # (status, output) = commands.getstatusoutput('clang -Xclang -ast-dump -fsyntax-only ' + code_path)
    return F

def Node_extract(code_path, preprocess):
    """Extract the nodes"""
    AST = AST_generate(code_path, preprocess)
    node_list = []
    new_line = ''
    for lines in AST:
        Node_dict = dict()
        if len(re.findall(RE_NODE, lines)) > 0:
            new_line = re.findall(RE_NODE, lines)[0]
        Node_dict['_nodetype'] = new_line
        line_info = re.findall(RE_LINE, lines)
        if len(line_info) > 0:
            Node_dict['coord'] = line_info[0]
        else:
            Node_dict['coord'] = 'null'
        node_list.append(Node_dict)
    return node_list





