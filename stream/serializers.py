import bson
import jsonschema
from django.http import Http404
from jsonschema import validate
from rest_framework import serializers

from .fields import ObjectIDField
from .models import Entry, Stream
from .validators import FieldsValueValidator


# Entry serializer
class EntrySerializer(serializers.ModelSerializer):
    _id = ObjectIDField(read_only=True)
    data = serializers.JSONField()

    class Meta:
        model = Entry
        fields = ("_id", "data")
        read_only_fields = ("_id",)

    def create(self, validated_data):
        stream_pk = self.context["view"].kwargs["stream_pk"]
        s = Stream.objects.get(pk=bson.ObjectId(stream_pk))
        validated_data["stream"] = s
        return super().create(validated_data)

    def validate(self, attrs):
        stream_pk = self.context["view"].kwargs["stream_pk"]
        try:
            s = Stream.objects.get(pk=bson.ObjectId(stream_pk))
        except Stream.DoesNotExist:
            raise Http404("Stream does not exist")
        try:
            _ = validate(instance=attrs["data"], schema=s.fields)
        except jsonschema.exceptions.ValidationError as e:
            raise serializers.ValidationError(
                f"The value provided ({attrs['data']}) did not match the schema: {s.fields}"
            ) from e

        return super().validate(attrs)


class StreamSerializer(serializers.ModelSerializer):
    _id = ObjectIDField(read_only=True)
    fields = serializers.JSONField(validators=[FieldsValueValidator])

    class Meta:
        model = Stream
        fields = ("_id", "name", "description", "fields")
        read_only_fields = ("_id",)
