from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = (
            'id', 'name'
        )


class GroupsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = (
            'id', 'name'
        )


class UserSerializer(serializers.ModelSerializer):
    permissions = PermissionSerializer(source='user_permissions', many=True, read_only=True)
    groups_list = GroupsSerializer(source='groups', many=True, read_only=True)

    class Meta:
        model = get_user_model()
        fields = (
            'id', 'username', 'first_name', 'last_name', 'email', 'user_permissions', 'permissions',
            'groups', 'groups_list'
        )