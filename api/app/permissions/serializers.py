from rest_framework import serializers
from django.contrib.auth.models import Permission
from django.contrib.auth.models import ContentType
from users.serializers import UserSerializer


class ContentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentType
        fields = ('id', 'app_label', 'model')
        read_only_fields = ('id', 'app_label', 'model')


class PermissionSerializer(serializers.ModelSerializer):
    users = UserSerializer(source='user_set', many=True, required=False)
    class Meta:
        model = Permission
        fields = (
            'id', 'name', 'codename', 'content_type', 'user_set', 'users'
        )


