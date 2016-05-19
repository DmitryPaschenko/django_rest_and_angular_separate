from django.conf.urls import url
from permissions import views


urlpatterns = [
    url(r'^$', views.PermList.as_view(), name='perm_list'),
    # url('^(?P<id>\d+)/$', views.SingleUser.as_view(), name='single_permission')
]