from rest_framework import serializers
from rest_framework.exceptions import APIException
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
        fields = ('id', 'name', 'template', 'widget', 'widget_metadata')


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
        fields = ('id', 'name', 'creators_group', 'creators_group_data', 'document_template_fields', 'document_template_steps', 'can_edit')

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


class DocumentValuesSerializer(DPDynamicFieldsModelSerializer, serializers.ModelSerializer):
    field = DocumentTemplateFieldSerializer(read_only=True)
    can_edit = serializers.SerializerMethodField()

    def get_can_edit(self, obj):
        return obj.can_edit()

    class Meta:
        model = DocumentValues
        fields = ('id', 'document', 'field', 'value', 'can_edit')


class DocumentSerializer(DPDynamicFieldsModelSerializer, serializers.ModelSerializer):
    template = DocumentTemplateSerializer(read_only=True)
    document_values = serializers.SerializerMethodField()

    def get_document_values(self, obj):
        user = self.context.get('request').user
        user_groups = [group.id for group in user.groups.all()]

        step = obj.get_current_step()

        if step and step.members_group.id in user_groups:
            read_only_fields_ids = [f.pk for f in step.readonly_fields.all()]
            editable_fields_ids = [f.pk for f in step.editable_fields.all()]
            queryset = DocumentValues.objects.filter(document=obj.id, field__in=read_only_fields_ids + editable_fields_ids)
        else:
            queryset = DocumentValues.objects.filter(pk__lte=0)

        serializer = DocumentValuesSerializer(instance=queryset, read_only=True, many=True)
        return serializer.data

    class Meta:
        model = Document
        fields = ('id', 'name', 'template', 'document_values')

    def create(self, validated_data):
        instance = Document()
        return self.update(instance, validated_data)

    def update(self, instance, validated_data):

        is_new = False
        instance.name = validated_data.get('name')

        if instance.pk is None:
            is_new = True
            template_id = self.initial_data.get('template', None)

            template = DocumentTemplate.objects.get(pk=template_id)
            if template_id is None or template is None:
                raise APIException('Template value is required')

            instance.template_id = template_id
            instance.step = instance.get_first_step()

        instance.save()

        if is_new:
            # Create and fill all template fields by default when create new document
            all_fields = DocumentTemplateField.objects.filter(template_id=instance.template_id)
            for field in all_fields:
                dv = DocumentValues(field_id=int(field.id))
                instance.document_values.add(dv)

        document_values = self.initial_data.get('document_values', None)
        if document_values:
            for document_value in document_values:
                field = document_value.get('field')
                field_id = field.get('id')
                if is_new:
                    f, created = DocumentValues.objects.get_or_create(document_id=instance.pk, field_id=int(field_id))
                else:
                    f = DocumentValues.objects.get(pk=document_value.get('id'))
                f.value = document_value.get('value')
                f.save()

        instance.update_calculated_fields()

        return instance