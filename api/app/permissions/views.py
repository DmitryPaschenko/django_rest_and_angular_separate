from permissions.serializers import PermissionSerializer, ContentTypeSerializer
from rest_framework.generics import ListCreateAPIView, ListAPIView
from django.contrib.auth.models import Permission, ContentType
from rest_framework.response import Response
from rest_framework import status
from rest_framework import filters
from dp_base_libs.paginations import DPAngularTablePagination


class PermissionList(ListCreateAPIView):
    serializer_class = PermissionSerializer
    pagination_class = DPAngularTablePagination
    queryset = Permission.objects.all()
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    ordering_fields = (
        'name', 'codename'
    )

    def post(self, request):
        try:
            serializer = self.get_serializer_class()(data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"detail":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Permission.DoesNotExist:
            return Response({}, status=status.HTTP_404_NOT_FOUND)


class ContentTypeList(ListAPIView):
    serializer_class = ContentTypeSerializer
    pagination_class = DPAngularTablePagination
    queryset = ContentType.objects.all()
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    ordering_fields = (
        'app_label', 'model'
    )

