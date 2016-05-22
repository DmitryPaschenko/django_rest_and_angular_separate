from django.conf.urls import url
from permissions import views


urlpatterns = [
    url(r'^$', views.PermissionList.as_view(), name='permission_list'),
    # url(r'contenttypes^$', views.ContentTypeList.as_view(), name='content_type_list'),
    # url('^(?P<id>\d+)/$', views.SingleUser.as_view(), name='single_permission')
]