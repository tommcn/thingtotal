import bson

from rest_framework import serializers


class ObjectIDField(serializers.Field):
    def to_representation(self, value):
        return str(value)

    def to_internal_value(self, data):
        return bson.ObjectId(data)
