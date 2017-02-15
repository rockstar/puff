import unittest

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

import puff


class AnThing(declarative_base()):
    """A test object for sqlalchemy validation."""
    __tablename__ = 'tester'

    id = Column(Integer, primary_key=True)

    foreign_id = Column(
        Integer, ForeignKey('foreign.id'), nullable=False)
    foreign = relationship('Foreign', foreign_keys=[foreign_id])

    name = Column(String(30), nullable=False)
    enabled = Column(Boolean, default=False)

    with_an_underscore = Column(String(1))


class AnThingValidator(puff.Validator):
    """A validator for AnThing."""

    class Meta:
        validates = AnThing
        fields = ['id', 'name', 'enabled']
        required = ['name', 'enabled']

        field_types = [
        ]


class TestValidator(unittest.TestCase):
    """Tests for puff.Validator.

    These tests use AnThing and AnThingValidator as the test api.
    """

    def test_validator_meta_attributes(self):
        """The Meta class attributes are available."""
        self.assertEqual(AnThing, AnThingValidator.Meta.validates)
        self.assertEqual(
            ['id', 'name', 'enabled'], AnThingValidator.Meta.fields)

    def test_schema_keys(self):
        """The validator schema is generated properly."""
        expected = ['$schema', 'properties', 'required', 'type']

        validator = AnThingValidator()

        self.assertEqual(expected, sorted(validator.schema.keys()))

    def test_schema_required(self):
        """The only requirement of the top-level schema is data."""
        validator = AnThingValidator()

        self.assertEqual(['data'], validator.schema['required'])

    def test_schema_data_keys(self):
        """The data keys and properties are generated."""
        expected = ['properties', 'required', 'type']

        validator = AnThingValidator()

        self.assertEqual(
            expected, sorted(validator.schema['properties']['data'].keys()))

    def test_schema_data_required(self):
        """The `type` and `attributes` are required in `data`."""
        validator = AnThingValidator()

        self.assertEqual(
            ['attributes', 'type'],
            sorted(validator.schema['properties']['data']['required']))

    def test_data_attributes_and_types(self):
        """The data attributes and types reflect the fields."""
        expected = {
            'id': {'type': 'integer'},
            'name': {'type': 'string'},
            'enabled': {'type': 'boolean'},
        }

        validator = AnThingValidator()
        attribs = validator.schema['properties']['data'][
            'properties']['attributes']['properties']

        self.assertEqual(expected, attribs)

    def test_data_attributes_required(self):
        """Required attributes are specified."""
        expected = ['enabled', 'name']

        validator = AnThingValidator()
        required = validator.schema['properties']['data'][
            'properties']['attributes']['required']

        self.assertEqual(expected, sorted(required))

    def test_underscore_to_hyphen(self):
        """Underscores with attributes are converted to hyphens."""

        class AnThingValidator2(puff.Validator):
            """A validator for AnThing."""

            class Meta:
                validates = AnThing
                fields = ['id', 'name', 'enabled', 'with_an_underscore']
                required = ['with_an_underscore']

        expected = {
            'id': {'type': 'integer'},
            'name': {'type': 'string'},
            'enabled': {'type': 'boolean'},
            'with-an-underscore': {'type': 'string'},
        }

        validator = AnThingValidator2()
        attribs = validator.schema['properties']['data'][
            'properties']['attributes']['properties']
        required = validator.schema['properties']['data'][
            'properties']['attributes']['required']

        self.assertEqual(expected, attribs)
        self.assertEqual(['with-an-underscore'], required)

    def test_field_types(self):
        """Field type will override the sqlalchemy column type."""

        class AnThingValidator2(puff.Validator):
            """A validator for AnThing."""

            class Meta:
                validates = AnThing
                fields = ['id', 'name', 'enabled']

                field_types = {
                    'enabled': 'string',
                }

        expected = {
            'id': {'type': 'integer'},
            'name': {'type': 'string'},
            'enabled': {'type': 'string'},
        }

        validator = AnThingValidator2()
        attribs = validator.schema['properties']['data'][
            'properties']['attributes']['properties']

        self.assertEqual(expected, attribs)
