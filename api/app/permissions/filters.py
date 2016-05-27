import django_filters
from django.contrib.auth.models import Permission
from rest_framework import filters


class PermissionFilter(filters.FilterSet):
    name = django_filters.CharFilter(name='name', lookup_expr='icontains')

    class Meta:
        model = Permission
        fields = ['name']