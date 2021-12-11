from rest_framework import serializers

from app.repo import initialize_repo

from repos.models import PR

repo = initialize_repo()


class PRCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PR
        fields = [
            'base',
            'compare',
            'title',
            'description',
            'status',
            'author_name',
            'author_email'
        ]

    def validate_base(self, value):
        branch_list = [branch.name for branch in list(repo.heads)]
        if value not in branch_list:
            raise serializers.ValidationError(
                f"Base branch '{value}' does not exist"
            )
        return value

    def validate_compare(self, value):
        branch_list = [branch.name for branch in list(repo.heads)]
        if value not in branch_list:
            raise serializers.ValidationError(
                f"Compare branch '{value}' does not exist"
            )
        return value


class PRListSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    description = serializers.SerializerMethodField()

    class Meta:
        model = PR
        fields = [
            'id',
            'title',
            'description',
            'status',
            'author_name',
            'author_email',
            'created_at'
        ]

    def get_description(self, obj):
        return obj.description[:100]


class PRUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PR
        fields = [
            'status',
        ]


class PRSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = PR
        fields = '__all__'
