import Get_Info.get_info_git as gt
import Get_Info.name_form as nf
import Get_Info.levenshtein as le
import re
import requests
import urllib
import urllib.error
import time


def request_api(api):
    app_key = '&key=ZEaUTt2btGSROV8q3NeOQg(('
    user_info = requests.get(api + app_key)
    user_info = user_info.json()
    return user_info


def request_source(source_url):
    request2 = urllib.request.Request(source_url)
    request2.add_header('user-agent', 'Chrome/51.0.2704.63 Safari/537.36')
    try:
        response2 = urllib.request.urlopen(request2)
        html2 = response2.read()
        user_source = html2.decode("utf8")
        response2.close()
    except urllib.error.HTTPError:
        print("Internal Server Error when requesting {}".format(source_url))
        return "null"
    return user_source


def InfoByName(name):
    Info = []
    default_info = {"display_name":"","location":"","user_id":0}
    #THe API returns info of all possible Stack Overflow usernames which contain the input name
    user_api = 'https://api.stackexchange.com/2.2/users' \
               '?pagesize=10&order=asc&min={}&sort=name&inname={}' \
               '&site=stackoverflow'.format(name,name)
    info = request_api(user_api)

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
    """"Get the associated github account from Stack Overflow users' profile"""
    default = "null"
    if not user_id == None:
        stk_url = 'https://stackoverflow.com/users/{}'.format(user_id)
        user_source = request_source(stk_url)
        if not user_source == "null":
            user_href = re.findall(r"<a.*?href=.*?<\/a>", user_source, re.I | re.S | re.M)
            # find it directly
            git_account = None
            for href in user_href:
                if 'https://github.com/' in href:
                    git_account = re.findall('href\=\"https\:\/\/github\.com\/(.*?)\"', href, re.S)
                    git_account = git_account[0]
            if not git_account == None:
                return git_account
            else:
                return default
        else:
            return default
    else:
        return default


def get_tags(stk_developer):
    """"Get the tags of Stack Overflow developer through API"""
    tags = []
    tags_api = 'https://api.stackexchange.com/2.2/users/{}/tags' \
               '?pagesize=100&order=desc&sort=popular' \
               '&site=stackoverflow'.format(stk_developer['user_id'])
    tags_info = request_api(tags_api)
    tags_info = tags_info["items"]
    for tag in tags_info:
        tag_name = tag["name"]
        tags.append(tag_name)
    return tags


def merge_langtopics(git_developer):
    topics_git = git_developer["github_topics"]
    language_git = git_developer["github_language"]
    if not topics_git == "null" and not language_git == "null":
        topics_git.extend(language_git)
        tags_git = topics_git
    elif topics_git == "null" and not language_git == "null":
        tags_git = language_git
    else:
        tags_git = topics_git
    git_developer["github_tags"] = tags_git
    return git_developer


def match_info(git_developer,stk_developer,syn_list,Threshold):
    """"The location and tags comparison"""
    location_stk = stk_developer["location"]
    location_git = git_developer["location"]

    if not location_git == "null" and not location_stk == "null":
        try:
            if location_git in location_stk:
                location_score = 1
            elif location_stk in location_git:
                location_score = 1
            else:
                # Levenshtein distance between two strings of location
                distance = le.lev(location_stk, location_git)
                len_git = max(len(location_git),len(location_stk))
                location_score = distance / len_git
        except TypeError:
            location_score = 0
    else:
        location_score = 0

    tags_git = git_developer["github_tags"]
    tags_stk = stk_developer["tags"]
    print("\n{} tags: {}".format(stk_developer["user_id"],tags_stk))

    match_count = github_count = 0
    if not tags_stk == [] and not tags_git == "null":
        match_tags = []
        for tag in tags_git:
            github_count = github_count + 1
            if tag in syn_list:
                stk_syn = syn_list[tag]
                if type(stk_syn) == list:
                    for syn_tags in stk_syn:
                        if syn_tags in tags_stk:
                            match_tags.append(syn_tags)
                            match_count = match_count + 1
                            break
                elif type(stk_syn) == str:
                    if stk_syn in tags_stk:
                        match_count = match_count + 1
        print("Match tag for {}: {}".format(stk_developer["display_name"],match_tags))
    else:
        match_count = 0
        github_count = 1

    tag_score = match_count / github_count * 2
    final_score = round(location_score + tag_score, 2)
    print("Final score for {}: {}".format(stk_developer["display_name"],final_score))

    if final_score >= Threshold:
        match_name = str(stk_developer["user_id"]) + "_" + str(final_score)
        return match_name
    else:
        return []


def match_account(git_info,syn_list):
    default_info = []
    new_info = []

    for git_developer in git_info:
        # Merge the languages and topics to github_tags
        git_developer = merge_langtopics(git_developer)
        print("\n\nFinding Github user {} on Stack Overflow...".format(git_developer["name"]))
        possible_name = nf.possible_names(git_developer["name"], git_developer["github_login"])
        print("Possible name:{}".format(possible_name))

        for name in possible_name:
            #All info of developers whose username contains the input name
            stk_info = InfoByName(name)
            stk_info = gt.delete_duplicate(stk_info)

            if not stk_info == default_info:
                print("The possible info of Stack Overflow user {} is {}".format(name, stk_info))
                cTime = time.time()

                for stk_developer in stk_info:
                    user_id = stk_developer['user_id']
                    git_account = GetGitAccount(user_id)

                    if git_account == git_developer["github_login"]:
                        git_developer["stackoverflow_login"] = stk_developer["display_name"]
                        print(time.time() - cTime)
                        break

                # Continue to establish mapping if the possible match has been found?
                if git_developer["stackoverflow_login"] == "null" or git_developer["stackoverflow_login"] == []:
                    git_developer["stackoverflow_login"] = []
                    print("\nNo linked account has been found. Mapping the users using tags and location...")
                    print("{} tags: {}".format(git_developer["github_login"], git_developer["github_tags"]))

                    cTime = time.time()
                    for stk_developer in stk_info:
                        developer_tags = get_tags(stk_developer)
                        stk_developer["tags"] = developer_tags
                        match_name = match_info(git_developer,stk_developer,syn_list,1)
                        if not match_name == []:
                            git_developer["stackoverflow_login"].append(match_name)
                    print(time.time() - cTime)
                else:
                    break

        if not git_developer["stackoverflow_login"] == "null" and not git_developer["stackoverflow_login"] == []:
            print("The Stack Overflow display_name for github user {}: {}".format(git_developer["name"],git_developer['stackoverflow_login']))
        else:
            git_developer["stackoverflow_login"] = "null"
            print("The Stack Overflow display_name for github user {} not found".format(git_developer["name"]))

        new_info.append(git_developer)
    return new_info





