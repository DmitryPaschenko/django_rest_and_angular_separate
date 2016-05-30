from rest_framework import serializers
from django.contrib.auth.models import Group
from users.serializers import UserSerializer


class GroupSerializer(serializers.ModelSerializer):
    users = UserSerializer(source='user_set', many=True, required=False)
    class Meta:
        model = Group
        fields = (
            'id', 'name', 'user_set', 'users'
        )