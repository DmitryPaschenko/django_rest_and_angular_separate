from users.serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework import status
from rest_framework.renderers import TemplateHTMLRenderer
import requests
from django.views.generic import TemplateView
from django.core.urlresolvers import reverse
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.contrib.auth import get_user_model
from rest_framework import filters
from django_filters import FilterSet, NumberFilter, IsoDateTimeFilter


class AccountConfirmEmailView(APIView):
    authentication_classes = ()
    permission_classes = ()
    renderer_classes = (TemplateHTMLRenderer, )

    def get(self, request, key, format=None):
        """
        Send confirmation request for given key and renders email confirmation status page.

            * key: verification key

            return: rendered HTML template 'account_confirm.html'
        """
        r = requests.post(
            request.build_absolute_uri(reverse('registration:rest_verify_email')),
            # 'http://localhost:{}/rest-auth/registration/verify-email/'.format(settings.SERVER_PORT),
            json={"key": key}
        )

        status = 'REGISTRATION COMPLETED' if r.status_code == 200 else r.raw

        return Response(
            {"status": status}, template_name='account_confirm.html', status=r.status_code
        )


class EmailVerificationSentView(APIView):
    authentication_classes = ()
    permission_classes = ()

    def get(self, request):
        return Response("Verification email has been sent.")


class SingleUser(GenericAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer

    def get(self, request, id):
        """
        Get user's data by it's id
        """
        try:
            user = self.get_queryset().get(pk=int(id))
        except get_user_model().DoesNotExist:
            return Response({}, status=status.HTTP_404_NOT_FOUND)

        user_data = self.get_serializer_class()(user, context={'request': request}).data

        return Response(user_data)


class UserListView(ListAPIView):
    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    ordering_fields = (
        'id', 'username', 'first_name', 'last_name', 'email'
    )





