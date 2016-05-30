import django_filters
from users.models import AppUser
from rest_framework import filters


class UserFilter(filters.FilterSet):
    username = django_filters.CharFilter(name='username', lookup_expr='icontains')
    first_name = django_filters.CharFilter(name='first_name', lookup_expr='icontains')
    last_name = django_filters.CharFilter(name='last_name', lookup_expr='icontains')
    email = django_filters.CharFilter(name='email', lookup_expr='icontains')
    exclude_ids = django_filters.MethodFilter(action='dp_exclude_filter')

    class Meta:
        model = AppUser
        fields = ['username', 'first_name', 'last_name', 'email', 'exclude_ids']

    def dp_exclude_filter(self, queryset, value):
        exclude_list = [];
        if value:
            exclude_list = value.split(',');

        return queryset.exclude(
            id__in=exclude_list
        )