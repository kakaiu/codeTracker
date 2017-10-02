import Get_Info.get_info_git as gt
import Get_Info.get_info_stackoverflow as st
import Get_Info.name_form as nf
import time
import json


git_api = 'https://api.github.com/repos/tensorflow/tensorflow/commits'
cTime = time.time()
git_info = gt.get_info(git_api)
info_file = '/home/ace/zsj/Get_Info/Info/git_info_list.json'
with open(info_file, 'w') as ctfile:
    json.dump(git_info, ctfile, indent=3)
print(time.time() - cTime)

# f = open(info_file,encoding='utf-8')
# git_info = json.load(f)

new_info = st.match_info(git_info)
with open(info_file, 'w') as ctfile:
    json.dump(new_info, ctfile, indent=3)

