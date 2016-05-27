import django_filters
from django.contrib.auth.models import Group
from rest_framework import filters


class GroupFilter(filters.FilterSet):
    name = django_filters.CharFilter(name='name', lookup_expr='icontains')

    class Meta:
        model = Group
        fields = ['name']