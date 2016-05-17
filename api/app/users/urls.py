from django.conf.urls import url
from users import views


urlpatterns = [
    url(r'^$', views.UserListView.as_view(), name='user_list'),
    url('^(?P<id>\d+)/$', views.SingleUser.as_view(), name='single_user')
]