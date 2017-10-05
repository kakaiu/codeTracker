import Get_Info.get_info_git as gt
import Get_Info.get_info_stackoverflow as st
import Get_Info.name_form as nf
import time
import json
import types

# git_api = 'https://api.github.com/repos/sindresorhus/awesome/commits'
# # git_api = 'https://api.github.com/repos/tensorflow/tensorflow/commits'
# git_info = gt.get_info(git_api)
info_file = '/home/ace/zsj/Get_Info/Info/git_info_awesome.json'
# cTime = time.time()
# print("Dumping the info...")
# with open(info_file, 'w') as ctfile:
#     json.dump(git_info, ctfile, indent=3)
# print(time.time() - cTime)

f = open(info_file,encoding='utf-8')
git_info = json.load(f)
stk_count = total_count = 0

new_info = st.match_info(git_info)
with open(info_file, 'w') as ctfile:
    json.dump(new_info, ctfile, indent=3)

for item in new_info:
    if not item["stackoverflow_login"] == "null":
        stk_count = stk_count + 1
    total_count = total_count +1

print("The number of developers with Stack Overflow account is {}".format(stk_count))
print("The number of developers is {}".format(total_count))
print("Ratio:{}".format(float(stk_count/total_count)))