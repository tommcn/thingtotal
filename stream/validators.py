import jsonschema
from jsonschema import validate
from rest_framework import serializers

schema = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "type": "array",
    "items": [
        {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "desc": {"type": "string"},
                "type": {"type": "string"},
            },
            "required": [
                "name",
                "desc",
            ],
        },
    ],
}


def FieldsValueValidator(value):
    try:
        val = validate(instance=value, schema=schema)
        print(val)
    except jsonschema.exceptions.ValidationError as e:
        raise serializers.ValidationError(
            f"The value provided ({value}) did not match the schema: {schema}"
        ) from e
