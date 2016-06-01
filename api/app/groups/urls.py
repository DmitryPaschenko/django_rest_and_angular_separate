from django.conf.urls import url
from groups import views


urlpatterns = [
    url(r'^$', views.GroupList.as_view(), name='group_list'),
    url('^(?P<pk>\d+)/$', views.SingleGroup.as_view(), name='single_group')
]