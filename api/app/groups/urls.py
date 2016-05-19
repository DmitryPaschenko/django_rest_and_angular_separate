from django.conf.urls import url
from groups import views


urlpatterns = [
    url(r'^$', views.GroupSerializer.as_view(), name='group_list'),
    # url('^(?P<id>\d+)/$', views.SingleUser.as_view(), name='single_permission')
]