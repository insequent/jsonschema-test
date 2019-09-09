#!/usr/bin/env python3
'''
Adds ability to set defaults in JSON validated by jsonschema

NOTE: Design is primarily from here: https://python-jsonschema.readthedocs.io/en/stable/faq/
'''
from jsonschema import Draft7Validator, validators


def extend_with_defaults(validator_class):
    validate_properties = validator_class.VALIDATORS["properties"]

    def set_defaults(validator, properties, instance, schema):
        for prop, subschema in properties.items():
            if "default" in subschema:
                instance.setdefault(prop, subschema["default"])

        for error in validate_properties(validator, properties, instance, schema):
            yield error

    return validators.extend(
        validator_class, {"properties": set_defaults},
    )


ValidateWithDefaults = extend_with_defaults(Draft7Validator)
