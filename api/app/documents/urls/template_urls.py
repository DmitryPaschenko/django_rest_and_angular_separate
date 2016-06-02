from django.conf.urls import url
from documents.views import document_template_views


urlpatterns = [
    url(r'^$', document_template_views.DocumentTemplateList.as_view(),
        name='document_template_list'),
    url('^(?P<pk>\d+)/$', document_template_views.SingleDocumentTemplate.as_view(),
        name='single_document_template'),
    url('^(?P<pk>\d+)/fields/$', document_template_views.DocumentTemplateFieldList.as_view(),
        name='document_template_field_list'),
]