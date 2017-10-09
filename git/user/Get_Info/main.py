import Get_Info.get_info_git as gt
import Get_Info.get_info_stackoverflow as st
import Get_Info.name_form as nf
import time
import json
import types

git_api = 'https://api.github.com/repos/sindresorhus/awesome/commits'
# git_api = 'https://api.github.com/repos/tensorflow/tensorflow/commits'
git_info = gt.get_info(git_api)
info_file = '/home/ace/zsj/Get_Info/Info/awesome_test.json'
syn_file = '/home/ace/zsj/Get_Info/Info/syn_list.json'
cTime = time.time()
print("Dumping the info...")
with open(info_file, 'w') as ctfile:
    json.dump(git_info, ctfile, indent=3)
print(time.time() - cTime)

# git_info = open(info_file,encoding='utf-8')
syn_list = open(syn_file,encoding='utf-8')
# git_info = json.load(git_info)
syn_list = json.load(syn_list)
stk_count = total_count = 0

cTime = time.time()
print("Matching developers between Github and Stack Overflow...")
match_info = st.match_account(git_info,syn_list)
print(time.time() - cTime)

cTime = time.time()
# new_info = []
for item in match_info:
    if not item["stackoverflow_login"] == "null":
        stk_count = stk_count + 1
    # new_info.append(item)
    total_count = total_count +1
print(time.time() - cTime)

print("The number of developers with Stack Overflow account is {}".format(stk_count))
print("The number of developers is {}".format(total_count))
print("Ratio:{}".format(float(stk_count/total_count)))

print("Saving the results of matching...")
cTime = time.time()
file = '/home/ace/zsj/Get_Info/Info/awesome_match.json'
with open(file, 'w') as ctfile:
    json.dump(match_info, ctfile, indent=3)
print(time.time() - cTime)