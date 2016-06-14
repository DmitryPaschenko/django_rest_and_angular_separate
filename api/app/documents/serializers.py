from rest_framework import serializers
from rest_framework.utils import model_meta
from users.serializers import UserSerializer
from groups.serializers import GroupSerializer
from dp_base_libs.serializers import DPDynamicFieldsModelSerializer, DPUpdateRelatedSerializerMixin
from documents.models import DocumentTemplate, DocumentTemplateField, DocumentTemplateStep, Document, DocumentValues
from django.contrib.auth.models import Group


class DocumentTemplateFieldSerializer(DPDynamicFieldsModelSerializer, serializers.ModelSerializer):
    template = serializers.PrimaryKeyRelatedField(queryset=DocumentTemplate.objects.all(), required=False)
    class Meta:
        model = DocumentTemplateField
        fields = ('id', 'name', 'template', 'widget')


class DocumentTemplateStepSerializer(DPDynamicFieldsModelSerializer, serializers.ModelSerializer):
    template = serializers.PrimaryKeyRelatedField(queryset=DocumentTemplate.objects.all(), required=False)
    members_group_data = GroupSerializer(source='members_group', read_only=True)

    editable_fields = DocumentTemplateFieldSerializer(many=True, read_only=True)
    readonly_fields = DocumentTemplateFieldSerializer(many=True, read_only=True)

    editable_fields_names = serializers.SlugRelatedField(
        source='editable_fields',
        many=True,
        read_only=True,
        slug_field='name'
    )
    readonly_fields_names = serializers.SlugRelatedField(
        source='readonly_fields',
        many=True,
        read_only=True,
        slug_field='name'
    )

    class Meta:
        model = DocumentTemplateStep
        fields = (
            'id', 'name', 'step_number', 'members_group', 'members_group_data', 'template',
            'editable_fields', 'readonly_fields', 'editable_fields_names', 'readonly_fields_names'
        )


class DocumentTemplateSerializer(DPUpdateRelatedSerializerMixin, DPDynamicFieldsModelSerializer,
                                 serializers.ModelSerializer):
    creators_group_data = GroupSerializer(source='creators_group', read_only=True)
    document_template_fields = DocumentTemplateFieldSerializer(many=True)
    document_template_steps = DocumentTemplateStepSerializer(many=True)

    class Meta:
        model = DocumentTemplate
        fields = ('id', 'name', 'creators_group', 'creators_group_data', 'document_template_fields', 'document_template_steps')

    def __update_related_objects(self, instance, data):
        template_fields = data.get('document_template_fields')
        template_steps = data.get('document_template_steps')

        self._update_related(pk_key='id', data=template_fields, model_class=DocumentTemplateField,
                             serializer_class=DocumentTemplateFieldSerializer, many=True,
                             base_instance=instance, related_name='template',
                             old_objects=instance.document_template_fields.all())

        self._update_related(pk_key='id', data=template_steps, model_class=DocumentTemplateStep,
                             serializer_class=DocumentTemplateStepSerializer, many=True,
                             base_instance=instance, related_name='template',
                             old_objects=instance.document_template_steps.all())

    def create(self, validated_data):
        instance = DocumentTemplate()
        return self.update(instance, validated_data)

    def update(self, instance, validated_data):
        validated_data.pop('document_template_fields')
        validated_data.pop('document_template_steps')

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Remove all related fields
        instance.document_template_fields.all().delete()
        instance.document_template_steps.all().delete()

        # Create New Related Fields
        fields = self.initial_data.get('document_template_fields')
        steps = self.initial_data.get('document_template_steps')

        field_associated = {}
        for field in fields:
            associated_key = field.get('name')
            field['template'] = instance
            new_field = DocumentTemplateField(**field)
            new_field.save()
            associated_value = new_field
            field_associated.update({associated_key: associated_value})

        for step in steps:
            editable_fields_names = step.pop('editable_fields_names', None)
            readonly_fields_names = step.pop('readonly_fields_names', None)

            new_step_data = {
                'template': instance,
                'step_number':  step.get('step_number'),
                'name': step.get('name'),
                'members_group': Group.objects.get(pk=step.get('members_group')),
            }
            new_step = DocumentTemplateStep(**new_step_data)
            new_step.save()

            for editable_field in editable_fields_names:
                field = field_associated.get(editable_field);
                if field:
                    new_step.editable_fields.add(field)

            for readonly_field in readonly_fields_names:
                field = field_associated.get(readonly_field);
                if field:
                    new_step.readonly_fields.add(field)



        return instance


class DocumentSerializer(DPDynamicFieldsModelSerializer, serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ('id', 'name', 'status', 'step')


class DocumentValuesSerializer(DPDynamicFieldsModelSerializer, serializers.ModelSerializer):
    class Meta:
        model = DocumentValues
        fields = ('id', 'document', 'field', 'value')