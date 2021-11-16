import json

import jsonschema
from jsonschema import validate
from rest_framework import serializers

with open("stream/schema/json-schema-v7.json", "r") as f:
    schema = json.load(f)


def FieldsValueValidator(value):
    try:
        _ = validate(instance=value, schema=schema)
    except jsonschema.exceptions.ValidationError as e:
        raise serializers.ValidationError(
            f"The value provided ({value}) did not match the schema: {schema}"
        ) from e
