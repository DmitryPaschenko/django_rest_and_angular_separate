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
    editors_group_data = GroupSerializer(source='editors_group', read_only=True)
    viewers_group_data = GroupSerializer(source='viewers_group', read_only=True)

    class Meta:
        model = DocumentTemplateStep
        fields = (
            'id', 'name', 'step_number', 'members_group', 'editors_group', 'viewers_group', 'members_group_data',
            'editors_group_data', 'viewers_group_data', 'template'
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
        validated_data.pop('document_template_fields')
        validated_data.pop('document_template_steps')

        ModelClass = self.Meta.model
        info = model_meta.get_field_info(ModelClass)
        many_to_many = {}
        for field_name, relation_info in info.relations.items():
            if relation_info.to_many and (field_name in validated_data):
                many_to_many[field_name] = validated_data.pop(field_name)

        try:
            instance = ModelClass.objects.create(**validated_data)
        except TypeError as exc:
            msg = (
                'Got a `TypeError` when calling `%s.objects.create()`. '
                'This may be because you have a writable field on the '
                'serializer class that is not a valid argument to '
                '`%s.objects.create()`. You may need to make the field '
                'read-only, or override the %s.create() method to handle '
                'this correctly.\nOriginal exception text was: %s.' %
                (
                    ModelClass.__name__,
                    ModelClass.__name__,
                    self.__class__.__name__,
                    exc
                )
            )
            raise TypeError(msg)

        # Save many-to-many relationships after the instance is created.
        if many_to_many:
            for field_name, value in many_to_many.items():
                setattr(instance, field_name, value)

        related_data = {
            'document_template_fields': self.initial_data.get('document_template_fields'),
            'document_template_steps': self.initial_data.get('document_template_steps')
        }
        self.__update_related_objects(instance, related_data)

        return instance

    def update(self, instance, validated_data):
        related_data = {
            'document_template_fields': self.initial_data.get('document_template_fields'),
            'document_template_steps': self.initial_data.get('document_template_steps')
        }

        validated_data.pop('document_template_fields')
        validated_data.pop('document_template_steps')

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        self.__update_related_objects(instance, related_data)

        return instance


class DocumentSerializer(DPDynamicFieldsModelSerializer, serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ('id', 'name', 'status', 'step')


class DocumentValuesSerializer(DPDynamicFieldsModelSerializer, serializers.ModelSerializer):
    class Meta:
        model = DocumentValues
        fields = ('id', 'document', 'field', 'value')