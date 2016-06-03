from rest_framework import serializers
from users.serializers import UserSerializer
from groups.serializers import GroupSerializer
from dp_base_libs.serializers import DPDynamicFieldsModelSerializer
from documents.models import DocumentTemplate, DocumentTemplateField, DocumentTemplateStep, Document, DocumentValues
from django.contrib.auth.models import Group


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

    def create(self, validated_data):
        template_fields = self.context.get('template_fields')
        template_steps = self.context.get('template_steps')
        template = DocumentTemplate.objects.create(**validated_data)

        for field_data in template_fields:
            field_data['template'] = template
            DocumentTemplateField.objects.create(**field_data)

        for step_data in template_steps:
            step_data['template'] = template
            step_data['members_group'] = Group.objects.get(id=step_data.get('members_group'))
            step_data['editors_group'] = Group.objects.get(id=step_data.get('editors_group'))
            step_data['viewers_group'] = Group.objects.get(id=step_data.get('viewers_group'))
            DocumentTemplateStep.objects.create(**step_data)

        return template


class DocumentSerializer(DPDynamicFieldsModelSerializer, serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ('id', 'name', 'status', 'step')


class DocumentValuesSerializer(DPDynamicFieldsModelSerializer, serializers.ModelSerializer):
    class Meta:
        model = DocumentValues
        fields = ('id', 'document', 'field', 'value')