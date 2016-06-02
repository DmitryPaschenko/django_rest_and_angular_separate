import django_filters
from rest_framework import filters
from documents.models import DocumentTemplate, DocumentTemplateField


class DocumentTemplateFilter(filters.FilterSet):
    name = django_filters.CharFilter(name='name', lookup_expr='icontains')

    class Meta:
        model = DocumentTemplate
        fields = ['name']


class DocumentTemplateFieldFilter(filters.FilterSet):
    name = django_filters.CharFilter(name='name', lookup_expr='icontains')

    class Meta:
        model = DocumentTemplateField
        fields = ['name', 'template', 'widget']