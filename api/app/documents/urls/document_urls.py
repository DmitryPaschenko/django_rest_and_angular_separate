from django.conf.urls import url
from documents.views import document_views


urlpatterns = [
    url(r'^$', document_views.DocumentList.as_view(),
        name='document_template_list'),
    url('^(?P<pk>\d+)/$', document_views.SingleDocument.as_view(),
        name='single_document'),
]