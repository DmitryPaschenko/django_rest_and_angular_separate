from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import filters
from rest_framework.exceptions import APIException
from dp_base_libs.paginations import DPAngularTablePagination
from documents.models import DocumentTemplate, DocumentTemplateField, DocumentTemplateStep
from documents.serializers import DocumentTemplateSerializer, DocumentTemplateFieldSerializer, DocumentTemplateStepSerializer
from documents.filters import DocumentTemplateFilter, DocumentTemplateFieldFilter
from dp_base_libs.decorators import exception_to_response


class DocumentTemplateList(ListCreateAPIView):
    serializer_class = DocumentTemplateSerializer
    pagination_class = DPAngularTablePagination
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_class = DocumentTemplateFilter
    ordering_fields = (
        'name'
    )

    def get_queryset(self):
        user = self.request.user
        user_groups = [group.id for group in user.groups.all()]
        # TODO this line OR with "Director Privilegy"(create this privilegy)
        queryset = DocumentTemplate.objects.filter(creators_group__in=user_groups)

        return queryset

    def post(self, request):
        try:
            serializer = self.get_serializer_class()(data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                raise ValueError(serializer.errors)
        except DocumentTemplate.DoesNotExist:
            return Response({}, status=status.HTTP_404_NOT_FOUND)


class SingleDocumentTemplate(RetrieveUpdateDestroyAPIView):
    serializer_class = DocumentTemplateSerializer

    def get_queryset(self):
        user = self.request.user
        user_groups = [group.id for group in user.groups.all()]
        # TODO this line OR with "Director Privilegy"(create this privilegy)
        queryset = DocumentTemplate.objects.filter(creators_group__in=user_groups)

        return queryset

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
                raise ValueError(serializer.errors)
        except DocumentTemplate.DoesNotExist:
            return Response({}, status=status.HTTP_404_NOT_FOUND)


class DocumentTemplateFieldList(ListCreateAPIView):
    serializer_class = DocumentTemplateFieldSerializer
    pagination_class = DPAngularTablePagination
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_class = DocumentTemplateFieldFilter
    ordering_fields = (
        'name'
    )

    # def get_queryset(self):
    #     # TODO this line OR with "Director Privilegy"(create this privilegy)
    #     return DocumentTemplateField.objects.all()
    def get_queryset(self):
        # TODO this line OR with "Director Privilegy"(create this privilegy)
        template_id = self.request.parser_context.get('kwargs').get('pk', None)

        if template_id is None:
            raise APIException('template_id required')

        user = self.request.user
        user_groups = [group.id for group in user.groups.all()]
        available_steps = DocumentTemplateStep.objects.filter(members_group__in=user_groups, template=template_id).order_by('step_number')

        if available_steps and len(available_steps) > 0:
            first_step = available_steps[0];
            editable_fields_ids = [f.pk for f in first_step.editable_fields.all()]

            return DocumentTemplateField.objects.filter(pk__in=editable_fields_ids)
        else:
            return DocumentTemplateField.objects.filter(pk__lte=0)

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
    serializer_class = DocumentTemplateFieldSerializer

    def get_queryset(self):
        return DocumentTemplateField.objects.all()

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