from django.conf.urls import include, url
from django.views.generic import TemplateView
from documents.urls import template_urls as document_template_url, template_field_urls, document_urls
from groups import urls as groups_api_url
from permissions import contenttypes_urls as contenttypes_api_urls
from permissions import permissions_urls as permissions_api_urls
from users import urls as user_api_urls


class MainView(TemplateView):
    template_name = 'index.html'

api_urls = [
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),
    # url(r'^perm/$', permissions_view.PermList.as_view()),
    url(r'^permissions/', include(permissions_api_urls, namespace="permissions")),
    url(r'^contenttypes/', include(contenttypes_api_urls, namespace="contenttypes")),
    url(r'^groups/', include(groups_api_url, namespace="groups")),
    url(r'^users/', include(user_api_urls)),

    url(r'^templates/', include(document_template_url, namespace="document_templates")),
    url(r'^template-fields/', include(template_field_urls, namespace="document_template_fields")),

    url(r'^documents/', include(document_urls, namespace="documents")),
]

urlpatterns = [
    # Rest Auth
    # API
    url(r'^api/v1/', include(api_urls)),
    url(r'^docs/', include('rest_framework_swagger.urls')),
    url(r'^$', MainView.as_view()),
]
