"""A library for validating SQLAlchemy-jsonapi apis."""
import copy
import functools

from jsonschema import validate as schema_validate, exceptions
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


def _user_error(status_code, message, title):
    """General user input error."""
    import flask
    from sqlalchemy_jsonapi import __version__ as jsonapi_version
    response = {
        'errors': [{
            'status': status_code,
            'source': {'pointer': '{0}'.format(flask.request.path)},
            'title': title,
            'detail': message,
        }],
        'jsonapi': {
            'version': '1.0'
        },
        'meta': {
            'sqlalchemy_jsonapi_version': jsonapi_version
        }
    }
    return flask.jsonify(response), status_code


# XXX: rockstar (14 Feb 2017) - The methods argument here is
# sub-optimal. Validation shouldn't be http method specific,
# but rather view specific. This is a side-effect of cramming
# logic for many different actions into a single view. Once
# that's fixed, we should remove the methods argument here.
def validate(validator, methods=None):
    def decorated(f):

        @functools.wraps(f)
        def _(*args, **kwargs):
            from flask import request
            if methods is None or request.method in methods:
                try:
                    schema_validate(request.json, validator().schema)
                except exceptions.ValidationError as err:
                    return _user_error(422, err.message, 'Invalid Body')
            return f(*args, **kwargs)
        return _
    return decorated
