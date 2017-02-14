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
                'attributes': {
                    'type': 'object',
                    'properties': None,
                    'required': None,
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
        fields = {}

        for field in self.Meta.fields:
            try:
                attr_type = _TYPE_MAP[
                    type(self.Meta.validates.__table__.c[field].type)]
            except KeyError:
                raise
            fields[field] = {'type': attr_type}

        schema = copy.deepcopy(_BASE_SCHEMA)
        schema['properties']['data'][
            'properties']['attributes']['properties'] = fields
        schema['properties']['data'][
            'properties']['attributes']['required'] = self.Meta.required
        return schema
