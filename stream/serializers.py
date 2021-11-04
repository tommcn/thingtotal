from rest_framework import serializers
from .models import Stream


# Stream serializer
class StreamSerializer(serializers.ModelSerializer):
    fields = serializers.JSONField()

    class Meta:
        model = Stream
        fields = ('_id', 'name', 'description', 'fields')
        read_only_fields = ('_id',)
