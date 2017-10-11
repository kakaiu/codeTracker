import Get_Info.get_info_git as gt
import Get_Info.get_info_stackoverflow as st
import Get_Info.name_form as nf
import time
import json
import types
import sys
import os

Info_path = sys.path[0] + "/Info"
if not os.path.exists(Info_path):
    os.mkdir(Info_path)

# name_file = Info_path + '/login_list.json'
# name_list = open(name_file,encoding='utf-8')
# name_list = json.load(name_list)
# git_info = gt.search_info(name_list)

info_file = Info_path + '/awesome_match_5.json'
syn_file = Info_path + '/syn_list.json'


git_info = open(info_file,encoding='utf-8')
syn_list = open(syn_file,encoding='utf-8')
git_info = json.load(git_info)
syn_list = json.load(syn_list)
stk_count = total_count = 0

cTime = time.time()
print("Matching developers between Github and Stack Overflow...")
match_info = st.match_account(git_info,syn_list)
print(time.time() - cTime)

for item in match_info:
    if not item["stackoverflow_login"] == "null":
        stk_count = stk_count + 1
    total_count = total_count +1

print("\n The number of developers with Stack Overflow account is {}".format(stk_count))
print("The number of developers is {}".format(total_count))
print("Ratio:{}".format(round(stk_count/total_count,4)))

print("Saving the results of matching...")
cTime = time.time()
file = Info_path + '/awesome_info_1.json'
with open(info_file, 'w') as ctfile:
    json.dump(match_info, ctfile, indent=3)
print(time.time() - cTime)