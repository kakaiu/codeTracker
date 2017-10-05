import Get_Info.get_info_git as gt
import re
import requests
import urllib
import Get_Info.name_form as nf

def request_api(api):
    user_info = requests.get(api)
    user_info = user_info.json()
    return user_info

def request_source(source_url):
    request2 = urllib.request.Request(source_url)
    request2.add_header('user-agent', 'Mozilla/5.0')
    response2 = urllib.request.urlopen(request2)
    html2 = response2.read()
    user_source = html2.decode("utf8")
    response2.close()
    return user_source

def InfoByName(name):
    Info = []
    default_info = {"display_name":"","location":"","user_id":0}
    user_api = 'https://api.stackexchange.com/2.2/users' \
               '?pagesize=10&order=asc&min={}&sort=name&inname={}' \
               '&site=stackoverflow&key=ZEaUTt2btGSROV8q3NeOQg(('.format(name,name)
    app_key = '&key=ZEaUTt2btGSROV8q3NeOQg(('
    #try:
    info = request_api(user_api + app_key)
    print(user_api)
    user_info = info["items"]
    if not user_info == None:
        for item in user_info:
            dict_info = {"display_name": item['display_name'],
                         "location": (item["location"] if "location" in item.keys() else "null"),
                         "user_id": item["user_id"]}
            Info.append(dict_info)
        Info = gt.delete_duplicate(Info)
        return Info
    else:
        return default_info

def GetGitAccount(user_id):
    default = "null"
    if not user_id == None:
        stk_url = 'https://stackoverflow.com/users/{}'.format(user_id)
        user_source = request_source(stk_url)
        # user_source = request_url(stk_url)
        user_href = re.findall(r"<a.*?href=.*?<\/a>", user_source, re.I | re.S | re.M)
        # find it directly?
        git_account = None
        for href in user_href:
            if 'https://github.com/' in href:
                git_account = re.findall('href\=\"https\:\/\/github\.com\/(.*?)\"', href, re.S)
                git_account = git_account[0]
                print(git_account)
        if not git_account == None:
            return git_account
        else:
            return default
    else:
        return default

def match_info(git_info):
    default_info = []
    new_info = []
    for git_developer in git_info:
        possible_name = nf.name_form(git_developer["name"], git_developer["login"])
        for name in possible_name:
            # the info of developers with the same name but different info
            stk_info = InfoByName(name)
            print(stk_info)
            if not stk_info == default_info:
                for stk_developer in stk_info:
                    user_id = stk_developer['user_id']
                    git_account = GetGitAccount(user_id)
                    if git_account == git_developer["login"]:
                        git_developer["stackoverflow_login"] = git_account
                        break
                if not git_developer["stackoverflow_login"] == "null":
                    break
            else:
                break

        if not git_developer["stackoverflow_login"] == "null":
            print("The Stack Overflow display_name for github user {} is {}".format(git_developer["name"],git_developer['stackoverflow_login']))
        else:
            print("The Stack Overflow display_name for github user {} not found".format(git_developer["name"]))

        new_info.append(git_developer)
    return new_info





