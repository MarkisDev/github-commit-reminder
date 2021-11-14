from github import Github
import datetime
import json
from notify_run import Notify
import schedule


def job():
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
    if (numCommits == 0):
        notify.send(f"{numCommits} commits pushed to {numRepos} repositories today!", f"https://github.com/{config['github_username']}")
    else:
        now = datetime.datetime.now()
        new = datetime.datetime(year=now.year, month=now.month, day=now.day,
                                hour=23, minute=59, second=0)
        diff = (new - now).total_seconds()
        m, s = divmod(diff, 60)
        h, m = divmod(m, 60)
        notify.send(
            f"You have {h:.0f}H : {m:.0f}M left to push commits!")


schedule.every(1).minutes.do(job)

while True:
    schedule.run_pending()
