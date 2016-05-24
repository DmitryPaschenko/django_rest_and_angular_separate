from django.conf.urls import url
from permissions import views


urlpatterns = [
    url(r'^$', views.PermissionList.as_view(), name='permission_list'),
    url('^(?P<id>\d+)/$', views.SinglePermission.as_view(), name='single_permission')
]