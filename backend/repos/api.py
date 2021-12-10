import time
from datetime import datetime

from git.exc import BadName, GitCommandError

from rest_framework import status, viewsets
from rest_framework.response import Response

from utils.mixins import BaseGenericViewSet

from app.repo import GitRepo
from app.urls import router

repo = GitRepo().repo


class BranchViewset(viewsets.GenericViewSet,
                    BaseGenericViewSet):
    """
    API endpoint to list branches and retrieve commits of a given branch.
    """

    lookup_field = 'branch'

    def list(self, request, *args, **kwargs):
        branch_list = [
            {"branch": branch.name.split('/')[1]}
            for branch in list(repo.remote().refs)[1:]
        ]
        return Response(branch_list, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        branch = kwargs.get('branch')
        try:
            commit_list = [
                {
                    "hash": commit.hexsha,
                    "message": commit.message,
                    "author": commit.author.name,
                    "timestamp": time.strftime(
                        '%Y-%m-%d %H:%M:%S', time.gmtime(commit.committed_date)
                    )
                }
                for commit in repo.iter_commits(branch)
            ]
            commit_list.sort(
                key=lambda i:
                    datetime.strptime(i["timestamp"], '%Y-%m-%d %H:%M:%S'),
                reverse=True
            )
            return Response(commit_list, status=status.HTTP_200_OK)
        except GitCommandError as gce:
            if f"fatal: bad revision '{branch}'" in str(gce):
                return Response(
                    {"message": f"Branch '{branch}' does not exist"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            else:
                print(gce.args)
        except Exception as e:
            print(type(e).__name__, e.args)

        return Response(
            {"message": "Internal Server Error"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class CommitViewset(viewsets.GenericViewSet,
                    BaseGenericViewSet):
    """
    API endpoint to retrieve commit details from a commit.
    """

    lookup_field = 'hash'

    def retrieve(self, request, *args, **kwargs):
        hash = kwargs.get('hash')
        print(hash)
        if hash is None:
            return Response(
                {"message": "Hash is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            commit = repo.commit(hash)
            commit_dict = {
                "hash": commit.hexsha,
                "message": commit.message,
                "timestamp": time.strftime(
                    '%Y-%m-%d %H:%M:%S', time.gmtime(commit.committed_date)
                ),
                "files_changed": [
                    {
                        "filename": file
                    }
                    for file in commit.stats.files
                ],
                "author_name": commit.author.name,
                "author_email": commit.author.email
            }
            return Response(commit_dict, status=status.HTTP_200_OK)
        except BadName:
            return Response(
                {"message": f"Hash '{hash}' does not exist"},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            print(type(e).__name__, e.args)

        return Response(
            {"message": "Internal Server Error"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


router.register(
    r'branches',
    BranchViewset,
    basename='branch'
)

router.register(
    r'commits',
    CommitViewset,
    basename='commit'
)
