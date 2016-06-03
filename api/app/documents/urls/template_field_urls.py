from django.conf.urls import url
from documents.views import document_template_views


urlpatterns = [
    url('^(?P<pk>\d+)/$', document_template_views.DocumentTemplateFieldList.as_view(), name='single_document_template')
]