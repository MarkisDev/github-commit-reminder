from github import Github
import datetime
import json
from notify_run import Notify

config = {}
data = {}
numCommits = numRepos = 0

with open('config-pr.json', 'r+', encoding='utf8') as f:
    config = json.load(f)

g = Github(config['access_token'])
notify = Notify(endpoint=f"https://notify.run/{config['notify_channel_id']}")

for repo in g.get_user().get_repos(visibility='all', sort="descending"):
    if (repo.updated_at.date() == datetime.datetime.utcnow().date()):
        # data[repo.full_name] = []
        numRepos += 1
        for commit in repo.get_commits():
            if commit.commit.author.date.date() == datetime.datetime.utcnow().date():
                # data[repo.full_name].append(commit.commit.message)
                numCommits += 1

notify.send(f"{numCommits} commits pushed to {numRepos} repositories today!", f"https://github.com/{config['github_username']}")
