import requests
import time
import json


def delete_duplicate(dict):
    Info = []
    for item in dict:
        if not item in Info:
            Info.append(item)
    return Info

def request_url(url,pagesize):
    app = '?per_page={}&client_id=ff50be78bda6f9fd0f2f' \
          '&client_secret=ef64972c0688bd6e7f9a15436e372053b95b44a0'.format(pagesize)
    res = requests.get(url+app)
    res.encoding = 'utf-8'
    info = res.json()
    return info

def extract_dict(res):
    # The info for comparsion with that in other open source community
    dict_info = {"name":res["name"],"github_login":res["login"],
                 "company":res["company"],"location":res["location"],
                 "email":res["email"],"stackoverflow_login":"null"}
    return dict_info

def get_langtags(user):
    language = []
    tags = []
    print("Finding languages used of github user: {}".format(user["github_login"]))
    repo_api = 'https://api.github.com/users/{}/repos'.format(user["github_login"])
    repos = request_url(repo_api,30)
    print("The repo API is {}".format(repo_api))

    for item in repos:
        print(item)
        #can be  parallel tags&language
        repo_name = item["name"]
        repo_tags = requests.get('https://api.github.com/repos/{}/{}/topics?'
                                 'per_page=10&client_id=ff50be78bda6f9fd0f2f'
                                 '&client_secret=ef64972c0688bd6e7f9a15436e372053b95b44a0'
                                 .format(user["github_login"],repo_name),
                                 headers = {"Accept":"application/vnd.github.mercy-preview+json"})
        repo_tags = repo_tags.json()["names"]
        tags.extend(repo_tags)

        if not item["languages_url"] == None:
            language_api = item["languages_url"]
            language_dict = request_url(language_api,100)
        else:
            language_dict = None
        language.extend(language_dict)

    tags = delete_duplicate(tags)
    language = delete_duplicate(language)

    print("Github user {} languages: {}".format(user["github_login"],language))
    print("Github user {} tags: {}".format(user["github_login"], tags))
    user["github_language"] = language
    user["github_tags"] = (tags if not tags == [] else "null")
    return user


def get_info(commit_api):
    developer_info = request_url(commit_api,5)
    Info = []
    cTime = time.time()
    print("Getting info of users in the commit history...")
    for item in developer_info:
        print(item)
        ### For a list of developers, find their url
        author_api = (item["author"]["url"] if not item["author"] == None else "null")
        committer_api = (item["committer"]["url"] if not item["committer"] == None else "null")

        if not author_api == "null":
            author_info = request_url(author_api,100)
            author_info = extract_dict(author_info)
            Info.append(author_info)

        if not committer_api == "null":
            committer_info = request_url(committer_api,100)
            committer_info = extract_dict(committer_info)
            Info.append(committer_info)

    print(time.time() - cTime)
    Info = delete_duplicate(Info)

    git_info = []
    cTime = time.time()
    for git_developer in Info:
        git_developer = get_langtags(git_developer)
        git_info.append(git_developer)
    print(time.time() - cTime)
    return git_info

def search_info(developer_login):
    Info = []
    for login in developer_login:
        api = 'https://api.github.com/users/{}'.format(login)
        developer_info = request_url(api,100)
        developer_info = extract_dict(developer_info)







if __name__ == '__main__':
    git_api = 'https://api.github.com/repos/sindresorhus/awesome/commits'
    # git_api = 'https://api.github.com/repos/tensorflow/tensorflow/commits'
    git_info = get_info(git_api)
    info_file = '/home/ace/zsj/Get_Info/Info/awesome_language.json'
    cTime = time.time()
    print("Dumping the info...")
    with open(info_file, 'w') as ctfile:
        json.dump(git_info, ctfile, indent=3)
    print(time.time() - cTime)


