#!/usr/bin/env python
import os

'''
    Preprocess of the code. Remove the header files and standard libraries
'''
code_path = './example/test.cc'
path_new = './example/test_new.cc'
with open(code_path , 'r') as f:
    lines = f.readlines()
f.close()

with open(path_new , 'w') as f_new:
    for line in lines:
        if '#include' in line:
            continue
        f_new.write(line)
f_new.close()

'''
    Print AST based on command line
'''
command = 'clang -Xclang -ast-dump -fsyntax-only ' + path_new
F = os.popen(command)
print F.read()
