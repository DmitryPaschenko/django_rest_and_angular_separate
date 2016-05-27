from permissions.serializers import PermissionSerializer, ContentTypeSerializer
from rest_framework.generics import ListCreateAPIView, ListAPIView, RetrieveUpdateAPIView
from django.contrib.auth.models import Permission, ContentType
from rest_framework.response import Response
from rest_framework import status
from rest_framework import filters
from dp_base_libs.paginations import DPAngularTablePagination
from permissions.filters import PermissionFilter


class PermissionList(ListCreateAPIView):
    serializer_class = PermissionSerializer
    pagination_class = DPAngularTablePagination
    queryset = Permission.objects.all()
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_class = PermissionFilter
    search_fields = ('name', 'codename')
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


class SinglePermission(RetrieveUpdateAPIView):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer

    def get(self, request, id):
        """
        Get user's data by it's id
        """
        try:
            permission = self.get_queryset().get(pk=int(id))
            data = self.get_serializer_class()(permission, context={'request': request}).data

            return Response(data)
        except Permission.DoesNotExist:
            return Response({}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, id):
        try:
            permission = self.get_queryset().get(pk=int(id))
            serializer = self.get_serializer_class()(permission, data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"detail":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Permission.DoesNotExist:
            return Response({}, status=status.HTTP_404_NOT_FOUND)


class ContentTypeList(ListAPIView):
    serializer_class = ContentTypeSerializer
    queryset = ContentType.objects.all()
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    ordering_fields = (
        'app_label', 'model'
    )

