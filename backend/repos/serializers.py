from rest_framework import serializers

from repos.models import PR


class CreatePRSerializer(serializers.ModelSerializer):
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


class ListPRSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    description = serializers.MethodField()

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


class PRSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = PR
        fields = '__all__'
