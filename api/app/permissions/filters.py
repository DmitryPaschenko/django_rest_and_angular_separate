import django_filters
from django.contrib.auth.models import Permission
from rest_framework import filters


class PermissionFilter(filters.FilterSet):
    name = django_filters.CharFilter(name='name', lookup_expr='icontains')
    exclude_ids = django_filters.MethodFilter(action='dp_exclude_filter')

    def dp_exclude_filter(self, queryset, value):
        exclude_list = [];
        if value:
            exclude_list = value.split(',');

        return queryset.exclude(
            id__in=exclude_list
        )

    class Meta:
        model = Permission
        fields = ['name', 'exclude_ids']