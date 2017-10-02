import Get_Info.get_info_git as gt
import re
import requests
import urllib
import Get_Info.name_form as nf

def request_url(url):
    request2 = urllib.request.Request(url)
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
               '&site=stackoverflow'.format(name,name)
    try:
        info = request_url(user_api)
        user_info = info.json()
        user_info = user_info["items"]
        for item in user_info:
            dict_info = {"display_name": item['display_name'],
                         "location": item["location"], "user_id": item["user_id"]}
            Info.append(dict_info)
        Info = gt.delete_duplicate(Info)
        return Info
    except:
        return default_info

def GetGitAccount(user_id):
    default = "null"
    if not user_id == None:
        try:
            stk_url = 'https://stackoverflow.com/users/{}'.format(1732559)
            user_source = request_url(stk_url)
            # user_source = request_url(stk_url)
            user_href = re.findall(r"<a.*?href=.*?<\/a>", user_source, re.I | re.S | re.M)
            # find it directly?
            for href in user_href:
                if 'https://github.com/' in href:
                    print(href)
                    git_account = re.findall(">(.*?)</a>", href, re.S)
                    print(git_account)
            if not git_account == None:
                return git_account
            else:
                return default
        except:
            return default
    else:
        return default

def match_info(git_info):
    default_info = {"display_name": "", "location": "", "user_id": 0}
    new_info = []
    for git_developer in git_info:
        possible_name = nf.name_form(git_developer["name"], git_developer["login"])
        for name in possible_name:
            # the info of developers with the same name but different info
            stk_info = InfoByName(name)
            if not stk_info == default_info:
                for stk_developer in stk_info:
                    print(stk_developer)
                    user_id = stk_developer['user_id']
                    git_account = GetGitAccount(user_id)
                    if git_account == git_developer["login"]:
                        git_developer["stackoverflow_login"] = git_account
                        break
                if not git_developer["stackoverflow_login"] == "null":
                    print("The Stack Overflow display_name for github user {} is {}".format(git_developer["name"]),
                          git_account)
                    break
            else:
                print("The Stack Overflow display_name for github user {} not found".format(git_developer["name"]))
                break
        new_info.append(git_developer)
    return new_info





