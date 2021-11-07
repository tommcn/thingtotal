
from rest_framework import serializers

from .models import Stream, Entry
from .validators import FieldsValueValidator
from .fields import ObjectIDField


# Entry serializer
class EntrySerializer(serializers.ModelSerializer):
    _id = ObjectIDField(read_only=True)
    data = serializers.JSONField()

    class Meta:
        model = Entry
        fields = ("_id", "data")
        read_only_fields = ("_id",)


class StreamSerializer(serializers.ModelSerializer):
    _id = ObjectIDField(read_only=True)
    fields = serializers.JSONField(validators=[FieldsValueValidator])

    class Meta:
        model = Stream
        fields = ("_id", "name", "description", "fields")
        read_only_fields = ("_id",)
