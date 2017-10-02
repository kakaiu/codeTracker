import requests
import types
import time


def delete_duplicate(dict):
    Info = []
    for item in dict:
        if not item in Info:
            Info.append(item)
    return Info

def request_url(url):
    app = '?per_page=100&client_id=8c3d71c8826d42e7cdf6' \
          '&client_secret=ae3a7ca2c74dffbf9558fff3b367e32e22140547'
    res = requests.get(url+app)
    info = res.json()
    return info

def extract_dict(res):
    # The info for comparsion with that in other open source community
    dict_info = {"name":res["name"],"login":res["login"],
                 "company":res["company"],"location":res["location"],
                 "email":res["email"],"stackoverflow_login":"null"}
    return dict_info

def get_info(commit_api):
    developer_info = request_url(commit_api)
    Info = []
    cTime = time.time()
    print("Getting info of users in the commit history...")
    for item in developer_info:
        author_api = item["author"]["url"]
        committer_api = item["committer"]["url"]

        author_info = request_url(author_api)
        author_info = extract_dict(author_info)

        committer_info = request_url(committer_api)
        committer_info = extract_dict(committer_info)

        Info.append(author_info)
        Info.append(committer_info)
    print(time.time() - cTime)
    Info = delete_duplicate(Info)
    return Info


