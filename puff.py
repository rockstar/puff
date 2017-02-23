"""A library for validating SQLAlchemy-jsonapi apis."""
import copy

from sqlalchemy.sql import sqltypes as types

_TYPE_MAP = {
    types.Integer: 'integer',
    types.String: 'string',
    types.Boolean: 'boolean',
}

_BASE_SCHEMA = {
    '$schema': 'http://json-schema.org/draft-04/schema#',
    'type': 'object',
    'properties': {
        'data': {
            'type': 'object',
            'properties': {
                'type': {
                    'type': 'string'
                },
                'id': {
                    'type': 'string'
                },
                'attributes': {
                    'type': 'object',
                    'properties': None,
                },
            },
            'required': [
                'type',
                'attributes'
            ],
        },
    },
    'required': [
        'data',
    ],
}


class Validator(object):
    """A class used for specifying validation information."""

    @property
    def schema(self):
        schema = copy.deepcopy(_BASE_SCHEMA)

        fields = {}
        for field in self.Meta.fields:
            try:
                if (hasattr(self.Meta, 'field_types')
                        and field in self.Meta.field_types):
                    attr_type = self.Meta.field_types[field]
                else:
                    attr_type = _TYPE_MAP[
                        type(self.Meta.validates.__table__.c[field].type)]
            except KeyError:
                raise
            fields[field.replace('_', '-')] = {'type': attr_type}
        schema['properties']['data'][
            'properties']['attributes']['properties'] = fields

        if hasattr(self.Meta, 'required') and len(self.Meta.required):
            required = [item.replace('_', '-') for item in self.Meta.required]
            schema['properties']['data'][
                'properties']['attributes']['required'] = required
        return schema
