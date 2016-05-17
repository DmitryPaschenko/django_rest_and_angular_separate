from django.conf.urls import include, url, patterns

api_urls = [
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),
]

urlpatterns = [
    # Rest Auth
    # API
    url(r'^api/v1/', include(api_urls)),
    url(r'^docs/', include('rest_framework_swagger.urls')),
]
