from rest_framework import serializers
from users.serializers import UserSerializer
from groups.serializers import GroupSerializer
from dp_base_libs.serializers import DPDynamicFieldsModelSerializer
from documents.models import DocumentTemplate, DocumentTemplateField, DocumentTemplateStep, Document, DocumentValues


class DocumentTemplateFieldSerializer(DPDynamicFieldsModelSerializer, serializers.ModelSerializer):
    class Meta:
        model = DocumentTemplateField
        fields = ('id', 'name', 'template', 'widget')


class DocumentTemplateStepSerializer(DPDynamicFieldsModelSerializer, serializers.ModelSerializer):
    members_group_data = GroupSerializer(source='members_group', read_only=True)
    editors_group_data = GroupSerializer(source='editors_group', read_only=True)
    viewers_group_data = GroupSerializer(source='viewers_group', read_only=True)

    class Meta:
        model = DocumentTemplateStep
        fields = (
            'id', 'name', 'step_number', 'members_group', 'editors_group', 'viewers_group', 'members_group_data',
            'editors_group_data', 'viewers_group_data', 'template'
        )


class DocumentTemplateSerializer(DPDynamicFieldsModelSerializer, serializers.ModelSerializer):
    creators_group_data = GroupSerializer(source='creators_group', read_only=True)
    template_fields = DocumentTemplateFieldSerializer(source='document_template_fields', many=True, read_only=True)
    template_steps = DocumentTemplateStepSerializer(source='document_template_steps', many=True, read_only=True)

    class Meta:
        model = DocumentTemplate
        fields = ('id', 'name', 'creators_group', 'creators_group_data', 'template_fields', 'template_steps')


class DocumentSerializer(DPDynamicFieldsModelSerializer, serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ('id', 'name', 'status', 'step')


class DocumentValuesSerializer(DPDynamicFieldsModelSerializer, serializers.ModelSerializer):
    class Meta:
        model = DocumentValues
        fields = ('id', 'document', 'field', 'value')