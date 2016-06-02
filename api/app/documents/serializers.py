from rest_framework import serializers
from users.serializers import UserSerializer
from dp_base_libs.serializers import DPDynamicFieldsModelSerializer
from documents.models import DocumentTemplate, DocumentTemplateField, DocumentStep, Document, DocumentValues


class DocumentTemplateSerializer(DPDynamicFieldsModelSerializer, serializers.ModelSerializer):
    creators_list = UserSerializer(source='creators', many=True, read_only=True)
    owner_data = UserSerializer(source='owner', read_only=True)

    class Meta:
        model = DocumentTemplate
        fields = ('id', 'name', 'owner', 'owner_data', 'creators', 'creators_list')


class DocumentTemplateFieldSerializer(DPDynamicFieldsModelSerializer, serializers.ModelSerializer):
    class Meta:
        model = DocumentTemplateField
        fields = ('id', 'name', 'template', 'widget')


class DocumentStepSerializer(DPDynamicFieldsModelSerializer, serializers.ModelSerializer):
    members_list = UserSerializer(source='members', many=True, read_only=True)
    editors_list = UserSerializer(source='editors', many=True, read_only=True)
    viewers_list = UserSerializer(source='viewers', many=True, read_only=True)

    class Meta:
        model = DocumentStep
        fields = (
            'id', 'name', 'step_number', 'members', 'editors', 'viewers', 'members_list', 'editors_list', 'viewers_list'
        )


class DocumentSerializer(DPDynamicFieldsModelSerializer, serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ('id', 'name', 'status', 'step')


class DocumentValuesSerializer(DPDynamicFieldsModelSerializer, serializers.ModelSerializer):
    class Meta:
        model = DocumentValues
        fields = ('id', 'document', 'field', 'value')