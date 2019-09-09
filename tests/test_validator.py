#!/usr/bin/env python
'''Tests for the validator'''
import io

import pytest
import yaml

from jsonschema_test.validator import ValidateWithDefaults


SCHEMAS = [
    ('''---
properties:
  name:
    type: string
    default: MyName
  id:
    type: integer
    default: 1
''', {'name': 'MyName', 'id': 1}),
    ('''---
properties:
  emails:
    type: array
    items:
      type: string
      format: email
    default: ["bob@email.com"]
''', {'emails': ['bob@email.com']}),
    ('''---
properties:
  id:
    type: string
    format: uuid
''', {})
]


@pytest.mark.parametrize("yaml_schema,expected", SCHEMAS)
def test_validator(yaml_schema, expected):
    with io.StringIO(yaml_schema) as buf:
        schema = yaml.safe_load(buf)

    result = {}
    ValidateWithDefaults(schema).validate(result)

    assert result == expected
