from django.conf.urls import url
from permissions import views


urlpatterns = [
    url(r'^$', views.ContentTypeList.as_view(), name='content_type_list'),
]