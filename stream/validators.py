import jsonschema
from jsonschema import validate

fieldsSchema = {"type": "object", "properties": {"description": {"type": "string"}}}


def FieldsValueValidator(value):
    try:
        validate(instance=value, schema=fieldsSchema)
    except jsonschema.exceptions.ValidationError as e:
        raise serializers.ValidationError(
            f"The value provided ({value}) did not match the schema: {fieldsSchema}"
        ) from e
