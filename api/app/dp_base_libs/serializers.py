from rest_framework import serializers


class DPDynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    Get only fields in "fields" request param
    "fields" parameter in request like ....&fields=id,name
    """

    def __init__(self, *args, **kwargs):
        super(DPDynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        fields = self.context.get('request').query_params.get('fields')
        if fields:
            fields = fields.split(',')
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)