#!/usr/bin/python
# -*- coding: UTF-8 -*-
#__author__ :king-jojo

import AST_Compare
from AST_Visualization import node_graph
import os
import sys

sel = True
code_path_a = './example/test.c'
json_name_a = './example/ast_a.json'

code_path_b = './example/test2.c'
json_name_b = './example/ast_b.json'

seq1 = AST_Compare.seq_process(code_path_a, json_name_a, sel)
seq2 = AST_Compare.seq_process(code_path_b, json_name_b, sel)
set = AST_Compare.Seqlist_compare(seq1,seq2)
node_graph(code_path_a, sel, set[0])
node_graph(code_path_b, sel, set[1])
