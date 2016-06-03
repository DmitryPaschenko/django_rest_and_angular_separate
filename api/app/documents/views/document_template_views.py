from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import filters
from dp_base_libs.paginations import DPAngularTablePagination
from documents.models import DocumentTemplate, DocumentTemplateField
from documents.serializers import DocumentTemplateSerializer, DocumentTemplateFieldSerializer, DocumentTemplateStepSerializer
from documents.filters import DocumentTemplateFilter, DocumentTemplateFieldFilter
from django.db import transaction


class DocumentTemplateList(ListCreateAPIView):
    serializer_class = DocumentTemplateSerializer
    pagination_class = DPAngularTablePagination
    queryset = DocumentTemplate.objects.all()
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_class = DocumentTemplateFilter
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
                return Response({"detail":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except DocumentTemplate.DoesNotExist:
            return Response({}, status=status.HTTP_404_NOT_FOUND)


# def post(self, request):
#     try:
#         fields = request.data.pop('template_fields')
#         steps = request.data.pop('template_steps')
#
#         template_serializer = self.get_serializer_class()(data=request.data, context={'request': request})
#         if template_serializer.is_valid():
#             template_serializer.save()
#             template_id = template_serializer.data.get('id')
#
#             # for field in fields:
#             #     field['template'] = template_id
#             field_serializer = DocumentTemplateFieldSerializer(data=fields, many=True)
#             if field_serializer.is_valid():
#                 field_serializer.save()
#             else:
#                 return Response({"detail": field_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
#
#             for step in steps:
#                 step['template'] = template_id
#             steps_serializer = DocumentTemplateStepSerializer(data=steps, many=True)
#             if steps_serializer.is_valid():
#                 steps_serializer.save()
#             else:
#                 return Response({"detail": steps_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
#
#             return Response(template_serializer.data, status=status.HTTP_200_OK)
#         else:
#             return Response({"detail": template_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
#     except DocumentTemplate.DoesNotExist:
#         return Response({}, status=status.HTTP_404_NOT_FOUND)


class SingleDocumentTemplate(RetrieveUpdateDestroyAPIView):
    queryset = DocumentTemplate.objects.all()
    serializer_class = DocumentTemplateSerializer

    def get(self, request, pk):
        """
        Get user's data by it's id
        """
        try:
            obj = self.get_queryset().get(pk=int(pk))
            data = self.get_serializer_class()(obj, context={'request': request}).data

            return Response(data)
        except DocumentTemplate.DoesNotExist:
            return Response({}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        try:
            obj = self.get_queryset().get(pk=int(pk))
            serializer = self.get_serializer_class()(obj, data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"detail":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except DocumentTemplate.DoesNotExist:
            return Response({}, status=status.HTTP_404_NOT_FOUND)





class DocumentTemplateFieldList(ListCreateAPIView):
    serializer_class = DocumentTemplateFieldSerializer
    pagination_class = DPAngularTablePagination
    queryset = DocumentTemplateField.objects.all()
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_class = DocumentTemplateFieldFilter
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
                return Response({"detail":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except DocumentTemplateField.DoesNotExist:
            return Response({}, status=status.HTTP_404_NOT_FOUND)


class SingleDocumentTemplateField(RetrieveUpdateDestroyAPIView):
    queryset = DocumentTemplateField.objects.all()
    serializer_class = DocumentTemplateFieldSerializer

    def get(self, request, pk):
        """
        Get user's data by it's id
        """
        try:
            obj = self.get_queryset().get(pk=int(pk))
            data = self.get_serializer_class()(obj, context={'request': request}).data

            return Response(data)
        except DocumentTemplateField.DoesNotExist:
            return Response({}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        try:
            obj = self.get_queryset().get(pk=int(pk))
            serializer = self.get_serializer_class()(obj, data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"detail":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except DocumentTemplateField.DoesNotExist:
            return Response({}, status=status.HTTP_404_NOT_FOUND)