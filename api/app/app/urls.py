from django.conf.urls import include, url
from users import urls as user_api_urls
from permissions import urls as permissions_api_urls
# from permissions import views as permissions_view
# from app.users

api_urls = [
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),
    # url(r'^perm/$', permissions_view.PermList.as_view()),
    url(r'^permissions/', include(permissions_api_urls, namespace="permissions")),
    url(r'^users/', include(user_api_urls)),
]

urlpatterns = [
    # Rest Auth
    # API
    url(r'^api/v1/', include(api_urls)),
    url(r'^docs/', include('rest_framework_swagger.urls')),
]
