from groups.serializers import GroupSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from dp_base_libs.paginations import DPAngularTablePagination
from django.contrib.auth.models import Group
from rest_framework import status
from rest_framework import filters
from groups.filters import GroupFilter
from rest_framework.response import Response
from users.permissions import DPChiefPermission


class GroupList(ListCreateAPIView):
    serializer_class = GroupSerializer
    pagination_class = DPAngularTablePagination
    queryset = Group.objects.all()
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_class = GroupFilter
    permission_classes = (DPChiefPermission,)
    ordering_fields = (
        'name'
    )

    def post(self, request):
        try:
            serializer = self.get_serializer_class()(data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Group.DoesNotExist:
            return Response({}, status=status.HTTP_404_NOT_FOUND)


class SingleGroup(RetrieveUpdateDestroyAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (DPChiefPermission,)

    def get(self, request, pk):
        """
        Get user's data by it's id
        """
        try:
            item = self.get_queryset().get(pk=int(pk))
            data = self.get_serializer_class()(item, context={'request': request}).data

            return Response(data)
        except Group.DoesNotExist:
            return Response({}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        try:
            item = self.get_queryset().get(pk=int(pk))
            serializer = self.get_serializer_class()(item, data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"detail":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Group.DoesNotExist:
            return Response({}, status=status.HTTP_404_NOT_FOUND)



