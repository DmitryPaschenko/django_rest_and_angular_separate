from permissions.serializers import PermissionSerializer
from rest_framework.generics import GenericAPIView, ListAPIView
from django.contrib.auth.models import Permission


class PermList(ListAPIView):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer




