Puff
====

A library for generating JSON Schema from SQLAlchemy objects.

Example
-------

Given the following SQLAlchemy model...

```
class AnThing(declarative_base()):
    """A test object for sqlalchemy validation."""
    __tablename__ = 'tester'

    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)
    enabled = Column(Boolean, default=False)
```

In this case, `name` and `enabled` are editable via the API, but id is not. A validator
would then be specified with the following. `enabled` is always required, as the API
is specifically for toggling the enabled bit, but could also be used to rename the
object as well.


```
import puff


class AnThingValidator(puff.Validator):
    class Meta:
        validates = AnThing
        fields = ['name', 'enabled']
        required = ['enabled']
```

Creating an instance of this object will provide a property that *is* the schema.


```
>>> AnThingValidator.schema['properties']['data']
```
