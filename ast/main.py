import AST_Process
import AST2JSON
import AST_Compare

code_path_a = './example/test.c'
json_name_a = './example/ast_a.json'
file_a = AST_Process.AST_generate(code_path_a,True)
source1 = AST_Process.Node_extract(file_a)
node_list_a = source1
dd_a = AST2JSON.to_json(node_list_a, json_name_a)
num_list_a = dd_a[0]
node_num_a = dd_a[1]

code_path_b = './example/test2.c'
json_name_b = './example/ast_b.json'
file_b = AST_Process.AST_generate(code_path_b,True)
source2 = AST_Process.Node_extract(file_b)
node_list_b = source2
dd_b = AST2JSON.to_json(node_list_b, json_name_b)
num_list_b = dd_b[0]
node_num_b = dd_b[1]

seq1 = AST_Compare.Sequence_generate(node_list_a, num_list_a)
seq2 = AST_Compare.Sequence_generate(node_list_b, num_list_b)
set = AST_Compare.Seqlist_compare(seq1,seq2)

"""show the same nodes that two programs share"""
print (set[0])
print (set[1])
print (node_num_a)
print (node_num_b)

#
#
# print (num_list_a)
# print (num_list_b)
# list = AST_Compare.Sequence_compare(seq1[0],seq2[0])
# list1 = list[1]
# list2 = list[2]
# print (list1)
# print (list2)
# print (list[0])
# print (seq1)
# print (seq2)
# print (source1)