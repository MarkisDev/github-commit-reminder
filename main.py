from github import Github
import datetime
import json

TOKEN = []

with open('config-pr.json', 'r+', encoding='utf8') as f:
    TOKEN = json.load(f)

g = Github(TOKEN['access_token'])

for repo in g.get_user().get_repos(visibility='all', sort="descending"):
    if (repo.updated_at.date() == datetime.datetime.utcnow().date()):
        for commit in repo.get_commits():
            if commit.commit.author.date.date() == datetime.datetime.utcnow().date():
                print(repo.full_name)
                print(commit.commit.message)
