#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os

def AST_preprocess(code_path):
    '''Preprocess of the code. Remove the header files and standard libraries'''
    path_new = './example/test_new.cc'
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

def AST_print(code_path):
    '''Print AST based on command line'''
    command = 'clang -Xclang -ast-dump -fsyntax-only ' + path
    F = os.popen(command)
    print (F.read())
