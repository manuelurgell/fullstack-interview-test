import time
from datetime import datetime

from git.exc import BadName, GitCommandError

from rest_framework import mixins, status, viewsets
from rest_framework.response import Response

from app.repo import initialize_repo
from app.urls import router

from repos import serializers
from repos.models import PR

from utils.mixins import (
    BaseGenericViewSet,
    CreateModelMixin,
    ListModelMixin,
    UpdateModelMixin
)

repo = initialize_repo()


class BranchViewset(viewsets.GenericViewSet,
                    BaseGenericViewSet):
    """
    API endpoint to list branches and retrieve commits of a given branch.
    """

    lookup_field = 'branch'

    def list(self, request, *args, **kwargs):
        branch_list = [
            {"branch": branch.name}
            for branch in list(repo.heads)
        ]
        return Response(branch_list, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        branch = self.request.query_params.get('branch')
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


class PRViewset(CreateModelMixin,
                ListModelMixin,
                mixins.RetrieveModelMixin,
                UpdateModelMixin,
                viewsets.GenericViewSet,
                BaseGenericViewSet):
    """
    API endpoint to create, list, and retrieve PRs.
    """
    serializer_class = serializers.PRSerializer
    create_serializer_class = serializers.PRCreateSerializer
    list_serializer_class = serializers.PRListSerializer
    update_serializer_class = serializers.PRUpdateSerializer

    queryset = PR.objects.all().order_by('-created_at')

    def create(self, request, *args, **kwargs):
        request.data["author_name"] = repo \
            .config_reader() \
            .get_value("user", "name")

        request.data["author_email"] = repo \
            .config_reader() \
            .get_value("user", "email")

        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        message = ""

        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=True, action='update'
        )
        serializer.is_valid(raise_exception=True)

        if request.data.get('status') == 'merged':
            try:
                base = repo.heads[instance.base]
                compare = repo.heads[instance.compare]

                base_commit = repo.merge_base(base, compare)
                repo.index.merge_tree(compare, base=base_commit)
                repo.index.commit(
                    f"Merged '{compare}' into '{base}'",
                    parent_commits=(base.commit, compare.commit)
                )
                compare.checkout(force=True)
                message = f"PR #{instance.id} merged successfully"
            except Exception as e:
                return Response(
                    {"message": e},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        if request.data.get('status') == 'closed':
            message = f"PR #{instance.id} closed successfully"

        serializer.save()
        return Response({"message": message}, status=status.HTTP_200_OK)


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

router.register(
    r'prs',
    PRViewset,
    basename='pr'
)
