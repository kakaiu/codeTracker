import requests
import time
import json
import multiprocessing

def delete_duplicate(dict):
    Info = []
    for item in dict:
        if not item in Info:
            Info.append(item)
    return Info

def request_url(url,pagesize):
    app = '?per_page={}&client_id=ff50be78bda6f9fd0f2f' \
          '&client_secret=ef64972c0688bd6e7f9a15436e372053b95b44a0'.format(pagesize)
    # cTime = time.time()
    res = requests.get(url+app)
    res.encoding = 'utf-8'
    info = res.json()
    # print("Requesting...:{}".format(time.time() - cTime))
    return info

def extract_dict(res):
    # The info for comparsion with that in other open source community
    dict_info = {"name":res["name"],"github_login":res["login"],
                 "company":res["company"],"location":res["location"],
                 "email":res["email"],"stackoverflow_login":"null"}
    return dict_info

def get_langtopics(user):
    # git_info = []
    language = []
    topics = []
    print("Finding languages and topics used by github user: {}".format(user["github_login"]))
    repo_api = 'https://api.github.com/users/{}/repos'.format(user["github_login"])
    repos = request_url(repo_api, 30)

    for item in repos:
        # can be  parallel topics & language
        repo_name = item["name"]
        # cTime = time.time()
        repo_topics = requests.get('https://api.github.com/repos/{}/{}/topics?'
                                   'per_page=10&client_id=ff50be78bda6f9fd0f2f'
                                   '&client_secret=ef64972c0688bd6e7f9a15436e372053b95b44a0'
                                   .format(user["github_login"], repo_name),
                                   headers={"Accept": "application/vnd.github.mercy-preview+json"})
        repo_topics = repo_topics.json()["names"]
        # print("Requesting...:{}".format(time.time() - cTime))
        topics.extend(repo_topics)

        if not item["languages_url"] == None:
            language_api = item["languages_url"]
            language_dict = request_url(language_api, 100)
        else:
            language_dict = None
        language.extend(language_dict)

    topics = delete_duplicate(topics)
    language = delete_duplicate(language)

    print("Github user {} languages: {}".format(user["github_login"], language))
    print("Github user {} topics: {}\n".format(user["github_login"], topics))
    user["github_language"] = language
    user["github_topics"] = (topics if not topics == [] else "null")
    return user


def get_info(developer_info):
    Info = []
    # for item in developer_info:
        ### For a list of developers, find their url
    item = developer_info
    if not item["author"]["login"] in Info:
        author_api = (item["author"]["url"] if not item["author"] == None else "null")
    else:
        author_api = "null"

    if not item["committer"]["login"] in Info:
        committer_api = (item["committer"]["url"] if not item["committer"] == None else "null")
    else:
        committer_api = "null"

    if not author_api == "null":
        author_info = request_url(author_api, 100)
        author_info = extract_dict(author_info)
        Info.append(author_info)

    if not committer_api == "null":
        committer_info = request_url(committer_api, 100)
        committer_info = extract_dict(committer_info)
        Info.append(committer_info)

    return Info

def search_info(developer_login):
    Info = []
    print("Getting info of users in the name list...")
    cTime = time.time()
    for login in developer_login:
        api = 'https://api.github.com/users/{}'.format(login)
        developer_info = request_url(api,100)
        developer_info = extract_dict(developer_info)
        Info.append(developer_info)
    print(time.time() - cTime)

    git_info = []
    cTime = time.time()
    for git_developer in Info:
        git_developer = get_langtopics(git_developer)
        git_info.append(git_developer)
    print(time.time() - cTime)
    return git_info

def multi_Prcapi(commit_api):
    developer_info = request_url(commit_api, 5)
    print("Getting info of user in the commit history...")

    cTime = time.time()
    pool = multiprocessing.Pool(processes=10)
    git_info = pool.map(get_info,developer_info)
    print(time.time() - cTime)
    pool.close()
    pool.join()
    merge_info = []
    for developer in git_info:
        merge_info.extend(developer)

    cTime = time.time()
    merge_info = delete_duplicate(merge_info)
    pool = multiprocessing.Pool(processes=10)
    merge_info = pool.map(get_langtopics,merge_info)
    print(time.time() - cTime)
    pool.close()
    pool.join()
    return merge_info

def multi_Prclist(name_list):
    print("Getting info of user in the commit history...")
    cTime = time.time()
    pool = multiprocessing.Pool(processes=10)
    git_info = pool.map(search_info,name_list)
    print(time.time() - cTime)
    pool.close()
    pool.join()
    merge_info = []
    for developer in git_info:
        merge_info.extend(developer)

    cTime = time.time()
    merge_info = delete_duplicate(merge_info)
    pool = multiprocessing.Pool(processes=10)
    merge_info = pool.map(get_langtopics,merge_info)
    print(time.time() - cTime)
    pool.close()
    pool.join()
    return merge_info



if __name__ == '__main__':
    git_api = 'https://api.github.com/repos/sindresorhus/awesome/commits'
    # git_api = 'https://api.github.com/repos/tensorflow/tensorflow/commits'

    git_info = multi_Prcapi(git_api)
    info_file = '/home/ace/zsj/GetInfo/Info/awesome_match_5.json'
    cTime = time.time()
    print("Dumping the info...")
    with open(info_file, 'w') as ctfile:
        json.dump(git_info, ctfile, indent=3)
    print(time.time() - cTime)


