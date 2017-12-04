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
import json

dir_path = os.path.dirname(os.path.realpath(__file__))

RE_AZ = re.compile(r'-(.*?) ')
RE_C = re.compile(r'/(.*?).c')
sel = True

if __name__ == '__main__':
    args = sys.argv[1:]
    if len(args)>0:
        if args[0] == '--compare':
            if len(args[1:]) == 3:
                if args[3] != 'True' and args[3] != 'False':
                    raise SystemExit("Please use 'True' or 'False' to choose whether you need to remove the headers")
                else:
                    if args[3] == 'True':
                        sel = True
                    else:
                        sel = False
                if os.path.exists(args[1]) and os.path.exists(args[2]):
                    code_path_a = args[1]
                    code_path_b = args[2]
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
                raise SystemExit("Usage: python main.py --compare c_file_dir1 c_file_dir2 True/False ")
        elif args[0] == '--view':
            if len(args[1:]) == 2:
                if args[2] != 'True' and args[2] != 'False':
                    raise SystemExit("Please use 'True' or 'False' to choose whether you need to remove the headers")
                else:
                    if args[2] == 'True':
                        sel = True
                    else:
                        sel = False
                if os.path.exists(args[1]):
                    code_path_a = args[1]
                    seq1 = AST_Compare.seq_process(code_path_a, sel)
                    node_graph(code_path_a, sel, None)
                else:
                    raise SystemExit("Error: Could not find c/c++ file")
            else:
                raise SystemExit("Usage: python main.py --view c_file_dir True/False ")
        elif args[0] == '--tojson':
            if len(args[1:]) == 2:
                if args[2] != 'True' and args[2] != 'False':
                    raise SystemExit("Please use 'True' or 'False' to choose whether you need to remove the headers")
                else:
                    if args[2] == 'True':
                        sel = True
                    else:
                        sel = False
                if os.path.exists(args[1]):
                    code_path = args[1]
                    if '.c' in code_path or '.cpp' in code_path:
                        node_list = Node_extract(code_path, sel)
                        print (node_list)
                        print ('The total amount of the nodes is {}'.format(len(node_list)))
                        json_files_dir = dir_path + '/jsons'
                        if not os.path.exists(json_files_dir):
                            os.mkdir(json_files_dir)
                        json_file = json_files_dir + '/output.json'
                        to_json(node_list, json_file, False)
                        print ("The json file path: "+json_files_dir)
                    else:
                        code_path_list = []
                        json_list = []
                        node_len = 0
                        g = os.walk(code_path)
                        for path, di, filelist in g:
                            for filename in filelist:
                                k = os.path.join(path, filename)
                                if '.c' in k or '.cpp' in k:
                                    code_path_list.append(k)
                        for i in range(len(code_path_list)):
                            node_list = Node_extract(code_path_list[i], sel)
                            name = re.findall(RE_C, code_path_list[i])
                            node_list.insert(0, name)
                            json_list.append(node_list)
                            node_len += len(node_list)
                        print ('The total amount of the nodes is {}'.format(node_len))
                        json_files_dir = dir_path + '/jsons'
                        if not os.path.exists(json_files_dir):
                            os.mkdir(json_files_dir)
                        json_file = json_files_dir + '/output.json'
                        to_json(json_list, json_file, True)
                        print ("The json file path: "+json_files_dir)
                else:
                    raise SystemExit("Error: Could not find c/c++ file")
            else:
                raise SystemExit("Usage: python main.py --tojson c_file_dir True/False")
        elif args[0] == '--combine':
            if len(args[1:]) == 2:
                if args[2] != 'True' and args[2] != 'False':
                    raise SystemExit("Please use 'True' or 'False' to choose whether you need to remove the headers")
                else:
                    if args[2] == 'True':
                        sel = True
                    else:
                        sel = False
                if os.path.exists(args[1]):
                    code_path = args[1]
                    node_graph(code_path, sel, None)
                else:
                    raise SystemExit("Error: Could not find the file")
            else:
                raise SystemExit("Usage: python main.py --combine c_file_dir1 c_file_dir2 True/False ")
        else:
            raise SystemExit("Usage: python main.py --compare c_file_dir1 c_file_dir2 True/False \n       python main.py --view c_file_dir True/False \n       python main.py --tojson c_file_dir True/False \n       python main.py --combine c_file_dir1 c_file_dir2 True/False  ")
    else:
        raise SystemExit("Usage: python main.py --compare c_file_dir1 c_file_dir2 True/False \n       python main.py --view c_file_dir True/False \n       python main.py --tojson c_file_dir True/False \n       python main.py --combine c_file_dir1 c_file_dir2 True/False  ")
