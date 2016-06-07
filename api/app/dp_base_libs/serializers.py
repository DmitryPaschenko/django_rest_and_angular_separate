from rest_framework import serializers


class DPDynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    Get only fields in "fields" request param
    "fields" parameter in request like ....&fields=id,name
    """

    def __init__(self, *args, **kwargs):
        super(DPDynamicFieldsModelSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request', None)
        if request is not None:
            fields = request.query_params.get('fields')
            if fields:
                fields = fields.split(',')
                allowed = set(fields)
                existing = set(self.fields.keys())
                for field_name in existing - allowed:
                    self.fields.pop(field_name)


class DPUpdateRelatedSerializerMixin(object):

    def __update_single_related(self, pk_key, model_class, serializer_class, data, base_instance, related_name):
        pk = data.get(pk_key, None)
        if pk is None:
            # add new related object
            data[related_name] = base_instance.pk
            serializer = serializer_class(data=data)
        else:
            # edit related object
            obj = model_class.objects.get(pk=int(pk))
            serializer = serializer_class(obj, data=data)

        if serializer.is_valid():
            serializer.save()
        else:
            raise ValueError('Related object save error')

    def __delete_related(self, pk_key, model_class, serializer_class, data, base_instance, related_name):
        pass

    def _update_related(self, pk_key, data, model_class, serializer_class, base_instance, related_name, many=False):
        if many:
            for single_data in data:
                self.__update_single_related(pk_key, model_class, serializer_class, single_data,
                                             base_instance, related_name)
        else:
            self.__update_single_related(pk_key, model_class, serializer_class, data, base_instance, related_name)