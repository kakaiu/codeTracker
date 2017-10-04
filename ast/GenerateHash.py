#!/usr/bin/python
# -*- coding: UTF-8 -*-
from __future__ import print_function
from pycparser import c_parser, c_ast
from PrintAST import AST_preprocess
from AST2JSON import write_json
import sys

file_name = './example/test.cc'
write_json(file_name)



