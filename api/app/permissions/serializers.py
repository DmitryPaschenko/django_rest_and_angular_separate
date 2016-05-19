from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission


class PermissionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Permission
        fields = (
            'id', 'name', 'codename'
        )