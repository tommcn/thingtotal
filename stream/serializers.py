import bson

from rest_framework import serializers

from .models import Stream, Entry
from .validators import FieldsValueValidator


class ObjectIDField(serializers.Field):
    def to_representation(self, value):
        return str(value)

    def to_internal_value(self, data):
        return bson.ObjectId(data)


# Entry serializer
class EntrySerializer(serializers.ModelSerializer):
    _id = ObjectIDField()
    data = serializers.JSONField()

    class Meta:
        model = Entry
        fields = ("_id", "data")
        read_only_fields = ("_id",)


class StreamSerializer(serializers.ModelSerializer):
    _id = ObjectIDField()
    fields = serializers.JSONField(validators=[FieldsValueValidator])

    class Meta:
        model = Stream
        fields = ("_id", "name", "description", "fields")
        read_only_fields = ("_id",)
