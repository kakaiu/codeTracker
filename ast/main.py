#!/usr/bin/python
# -*- coding: UTF-8 -*-

__author__ = 'king-jojo'

import AST_Compare
from AST_Visualization import node_graph
from AST2JSON import to_json
from AST_Process import Node_extract
import sys
import os
import re

dir_path = os.path.dirname(os.path.realpath(__file__))

RE_AZ = re.compile(r'-(.*?) ')
RE_C = re.compile(r'/(.*?).c')

if __name__ == '__main__':
    args = sys.argv[1:]
    if len(args)>0:
        if args[0] == '--compare':
            if len(args[1:]) == 2:
                if os.path.exists(args[1]) and os.path.exists(args[2]):
                    code_path_a = args[1]
                    code_path_b = args[2]
                    sel = True
                    seq1 = AST_Compare.seq_process(code_path_a, sel)
                    seq2 = AST_Compare.seq_process(code_path_b, sel)
                    set = AST_Compare.Seqlist_compare(seq1, seq2)
                    node_graph(code_path_a, sel, set[0])
                    node_graph(code_path_b, sel, set[1])
                if not os.path.exists(args[1]) and os.path.exists(args[2]):
                    raise SystemExit("Error: Could not find the first c/c++ file")
                if not os.path.exists(args[2]) and os.path.exists(args[1]):
                    raise SystemExit("Error: Could not find the second c/c++ file")
                if not os.path.exists(args[1]) and not os.path.exists(args[2]):
                    raise SystemExit("Error: Could not find both two files")
            else:
                raise SystemExit("Usage: python main.py --compare c_file_dir1 c_file_dir2")
        elif args[0] == '--view':
            if len(args[1:]) == 1:
                if os.path.exists(args[1]):
                    code_path_a = args[1]
                    sel = True
                    seq1 = AST_Compare.seq_process(code_path_a, sel)
                    node_graph(code_path_a, sel, None)
                else:
                    raise SystemExit("Error: Could not find c/c++ file")
            else:
                raise SystemExit("Usage: python main.py --view c_file_dir")
        elif args[0] == '--tojson':
            if len(args[1:]) == 1:
                if os.path.exists(args[1]):
                    code_path_a = args[1]
                    sel = True
                    node_list = Node_extract(code_path_a, sel)
                    json_files_dir = dir_path + '/jsons'
                    if not os.path.exists(json_files_dir):
                        os.mkdir(json_files_dir)
                    json_file = json_files_dir + '/output.json'
                    to_json(node_list, json_file)
                    print ("The json file path: "+json_files_dir)
                else:
                    raise SystemExit("Error: Could not find c/c++ file")
            else:
                raise SystemExit("Usage: python main.py --tojson c_file_dir")
        else:
            raise SystemExit("Usage: python main.py --compare c_file_dir1 c_file_dir2 \n       python main.py --view c_file_dir \n       python main.py --tojson c_file_dir ")
    else:
        raise SystemExit("Usage: python main.py --compare c_file_dir1 c_file_dir2 \n       python main.py --view c_file_dir \n       python main.py --tojson c_file_dir ")