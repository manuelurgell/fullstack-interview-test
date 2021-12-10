from django.conf import settings

from git import Repo
from git.exc import GitCommandError


class GitRepo(Repo):
    _instance = None
    try:
        repo = Repo.clone_from(
            'https://github.com/manuelurgell/fullstack-interview-test',
            'fullstack-interview-test'
        )
    except GitCommandError as gce:
        if "fatal: destination path 'fullstack-interview-test' already exists and is not an empty directory" in str(gce):  # noqa: E501
            repo = Repo('fullstack-interview-test')
        else:
            print(type(gce).__name__, gce.args)
            raise gce

    repo.config_writer().set_value(
        "user", "name", settings.GITHUB_USER_NAME
    ).release()
    repo.config_writer().set_value(
        "user", "email", settings.GITHUB_USER_NAME
    ).release()
