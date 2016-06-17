from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import filters
from dp_base_libs.paginations import DPAngularTablePagination
from documents.models import Document
from documents.serializers import DocumentSerializer
from rest_framework.decorators import api_view


class DocumentList(ListCreateAPIView):
    serializer_class = DocumentSerializer
    pagination_class = DPAngularTablePagination
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    # filter_class = DocumentTemplateFilter
    ordering_fields = (
        'name'
    )

    def get_queryset(self):
        # Available document STEP
        user = self.request.user
        user_groups = [group.id for group in user.groups.all()]
        queryset = Document.objects.filter(step__members_group__in=user_groups)

        return queryset

    def post(self, request):
        try:
            serializer = self.get_serializer_class()(data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                raise ValueError(serializer.errors)
        except Document.DoesNotExist:
            return Response({}, status=status.HTTP_404_NOT_FOUND)


class SingleDocument(RetrieveUpdateDestroyAPIView):
    serializer_class = DocumentSerializer

    def get_queryset(self):
        # Available document STEP
        user = self.request.user
        user_groups = [group.id for group in user.groups.all()]
        queryset = Document.objects.filter(step__members_group__in=user_groups)

        return queryset

    def get(self, request, pk):
        """
        Get user's data by it's id
        """
        try:
            obj = self.get_queryset().get(pk=int(pk))
            data = self.get_serializer_class()(obj, context={'request': request}).data

            return Response(data)
        except Document.DoesNotExist:
            return Response({}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        try:
            obj = self.get_queryset().get(pk=int(pk))
            serializer = self.get_serializer_class()(obj, data=request.data, context={'request': request})

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                raise ValueError(serializer.errors)
        except Document.DoesNotExist:
            return Response({}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def next_step(request, pk):
    try:
        d = Document.objects.get(pk=pk)
        d.next_step(request.user)
        return Response({}, status=status.HTTP_200_OK)
    except Document.DoesNotExist:
        raise Response({}, status=status.HTTP_404_NOT_FOUND)
